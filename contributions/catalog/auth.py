import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db
from .config import Config

# from oic.oic import Client
# from oic.utils.authn.client import CLIENT_AUTHN_METHOD
# from oic.oic.message import AuthorizationResponse
# from oic.oic.message import RegistrationResponse
# from oic import rndstr
# from oic.utils.http_util import Redirect
#

# bp = Blueprint('auth', __name__, url_prefix=Config.URL_PREFIX + '/auth')
bp = Blueprint('auth', __name__, url_prefix='/auth')
# client = Client(client_authn_method=CLIENT_AUTHN_METHOD)
# provider_info = client.provider_config(Config.ISSUER_URL)
# info = {"client_id": Config.CLIENT_ID, "client_secret": Config.CLIENT_SECRET, "redirect_uris": Config.REDIRECT_URIS}
# client_reg = RegistrationResponse(**info)
# client.store_registration_info(client_reg)
#
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        flash(error)
    return render_template('auth/register.html')



def check_login(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        access = session.get("access")
        if access is not None:
            if Config.ROLE.get(access) is not None:
                return redirect(Config.ROLE.get(access)[1])
        return view(**kwargs)

    return wrapped_view


def role_required(role):
    def decorator(view):
        @functools.wraps(view)
        def decorated_function(**kwargs):
            access = session.get("access")
            if access is None:
                return redirect(url_for("auth.login"))
            else:
                if Config.ROLE.get(access) is not None:
                    if Config.ROLE.get(access)[0] < Config.ROLE.get(role)[0] and access != role:
                        return redirect(Config.ROLE.get(access))[1]
                else:
                    return redirect(url_for("auth.login"))
                return view(**kwargs)
        return decorated_function
    return decorator



def login_shibboleth():
    session["state"] = rndstr()
    session["nonce"] = rndstr()
    args = {
        "client_id": client.client_id,
        "response_type": "code",
        "scope": Config.SCOPES,
        "nonce": session["nonce"],
        "redirect_uri": client.registration_response["redirect_uris"][0],
        "state": session["state"]
    }
    auth_req = client.construct_AuthorizationRequest(request_args=args)
    login_url = auth_req.request(client.authorization_endpoint)
    return Redirect(login_url)


@bp.route('/login')
@check_login
def login():
    if Config.LOGIN_MODE == "shibboleth":
        return login_shibboleth()


@bp.route('/callback')
def callback():
    if Config.LOGIN_MODE != "shibboleth":
        return redirect(url_for("auth.login"))
    response = request.environ["QUERY_STRING"]
    authentication_response = client.parse_response(AuthorizationResponse, info=response, sformat="urlencoded")
    code = authentication_response["code"]
    assert authentication_response["state"] == session["state"]
    args = {"code": code}
    token_response = client.do_access_token_request(state=authentication_response["state"],
                                                    request_args=args,
                                                    authn_method="client_secret_basic")
    user_info = client.do_user_info_request(state=authentication_response["state"])

    rokwireAuth = list(filter(
        lambda x: "urn:mace:uiuc.edu:urbana:authman:app-rokwire-service-policy-" in x,
        user_info.to_dict()["uiucedu_is_member_of"]
    ))
    # if user has no privilege
    # TODO: add a warning bar
    if len(rokwireAuth) == 0:
        return redirect(url_for("auth.login"))
    else:
        # fill in user information
        session["name"] = user_info.to_dict()["name"]
        session["email"] = user_info.to_dict()["email"]
        # check for corresponding privilege
        isUserAdmin = False
        isSourceAdmin = False
        for tag in rokwireAuth:
            if "rokwire em user events admins" in tag:
                isUserAdmin = True
            if "rokwire em calendar events admins" in tag:
                isSourceAdmin = True
        # TODO: we are storing cookie by our own but not by code, may change it later
        if isUserAdmin and isSourceAdmin:
            session["access"] = "both"
            session.permanent = True
            return redirect(url_for("auth.select_events"))
        elif isUserAdmin:
            session["access"] = "user"
            session.permanent = True
            return redirect(url_for("user_events.user_events"))
        elif isSourceAdmin:
            session["access"] = "source"
            session.permanent = True
            return redirect(url_for("event.source", sourceId=0))
        else:
            # TODO: add a warning bar
            session.clear()
            return redirect(url_for("auth.login"))


@bp.route('/select-events', methods=['GET', 'POST'])
@role_required("both")
def select_events():
    if request.method == 'POST':
        event = request.form.get("event")
        if event == "user":
            return redirect(url_for("user_events.user_events"))
        elif event == "source":
            return redirect(url_for("event.source", sourceId=0))
        else:
            return render_template("auth/select-events.html")
    return render_template("auth/select-events.html")


@bp.before_app_request
def load_logged_in_user_info():
    if session.get("access") is None:
        g.user = None
    else:
        g.user = {}
        g.user["access"] = session["access"]
        g.user["username"] = session["name"]


@bp.route('/logout')
@role_required('either')
def logout():
    session.clear()
    return redirect(url_for('home.home'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view
