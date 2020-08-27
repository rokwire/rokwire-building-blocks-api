import os

from flask import Flask, request, g, redirect, url_for
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user
)
from oic import rndstr
from oic.oic import Client
from oic.oic.message import AuthorizationResponse, RegistrationResponse, ClaimsRequest, Claims
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from oic.utils.http_util import Redirect

from user import User

app = Flask(__name__)
app.secret_key = os.urandom(24)

# OIDC setting
app.config.from_pyfile('config.py', silent=True)

# create oidc client
client = Client(client_authn_method=CLIENT_AUTHN_METHOD)

# get authentication provider details by hitting the issuer URL
provider_info = client.provider_config(app.config["ISSUER_URL"])

# store registration details
info = {
    "client_id": app.config["CLIENT_ID"],
    "client_secret": app.config["CLIENT_SECRET"],
    "redirect_uris": app.config["REDIRECT_URIS"]
}
client_reg = RegistrationResponse(**info)
client.store_registration_info(client_reg)

session = dict()

# LOGIN management setting
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.teardown_appcontext
def close_connection(exception):
    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()


@app.route('/login')
def login():
    session['state'] = rndstr()
    session['nonce'] = rndstr()

    # setup claim request
    claims_request = ClaimsRequest(
        userinfo=Claims(uiucedu_uin={"essential": True})
    )

    args = {
        "client_id": client.client_id,
        "response_type": "code",
        "scope": app.config["SCOPES"],
        "nonce": session["nonce"],
        "redirect_uri": client.registration_response["redirect_uris"][0],
        "state": session["state"],
        "claims": claims_request
    }

    auth_req = client.construct_AuthorizationRequest(request_args=args)
    login_url = auth_req.request(client.authorization_endpoint)

    return Redirect(login_url)


@app.route('/callback')
def callback():
    response = request.environ["QUERY_STRING"]

    authentication_response = client.parse_response(AuthorizationResponse, info=response, sformat="urlencoded")

    code = authentication_response["code"]
    assert authentication_response["state"] == session["state"]

    args = {
        "code": code
    }

    token_response = client.do_access_token_request(state=authentication_response["state"], request_args=args,
                                                    authn_method="client_secret_basic")

    user_info = client.do_user_info_request(state=authentication_response["state"])

    # see if that user is in local database or not
    user = User.search(user_info["preferred_username"])

    # create that user in local db if that person is not there;
    if not user:
        user = User.create(netid=user_info["preferred_username"], fname=user_info["given_name"],
                           lname=user_info["family_name"], email=user_info["email"], uin=user_info["uiucedu_uin"],
                           phone="NA")

    # checking user info - TODO
    rokwireAuth = list(filter(
        lambda x: "urn:mace:uiuc.edu:urbana:authman:app-rokwire-service-policy-" in x,
        user_info.to_dict()["uiucedu_is_member_of"]
    ))

    if len(rokwireAuth) == 0:
        return redirect(url_for("auth.login"))
    else:
        login_user(user)

    return redirect(url_for("home"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
