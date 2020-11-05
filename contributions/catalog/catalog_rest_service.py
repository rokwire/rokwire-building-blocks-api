<<<<<<< HEAD
import logging
import os
from time import gmtime

=======
import json
import logging
import os
import random
import string
from time import gmtime
import requests
>>>>>>> task/580-contribution-catalog-auth
from controllers.auth import bp as auth_bp
from controllers.config import Config as cfg
from controllers.contribute import bp as contribute_bp
from db import init_app
<<<<<<< HEAD
from flask import Flask, render_template
=======
from flask import Flask, jsonify, redirect, render_template, request, make_response
from flask import session as login_session
>>>>>>> task/580-contribution-catalog-auth

debug = cfg.DEBUG

log = logging.getLogger('werkzeug')
log.disabled = True

logging.Formatter.converter = gmtime
log_format = '%(asctime)-15s.%(msecs)03dZ %(levelname)-7s [%(threadName)-10s] : %(name)s - %(message)s'

if debug:
    logging.basicConfig(datefmt='%Y-%m-%dT%H:%M:%S', format=log_format, level=logging.DEBUG)
else:
    logging.basicConfig(datefmt='%Y-%m-%dT%H:%M:%S', format=log_format, level=logging.INFO)
if cfg and cfg.URL_PREFIX:
    prefix = cfg.URL_PREFIX
    staticpath = prefix + '/static'
else:
    staticpath = '/static'

template_dir = os.path.join(os.path.abspath('webapps'), 'templates')
static_dir = os.path.join(os.path.abspath('webapps'), 'static')
app = Flask(__name__, instance_relative_config=True, static_url_path=staticpath, static_folder=static_dir,
            template_folder=template_dir)
app.config.from_object(cfg)

init_app(app)
app.register_blueprint(auth_bp)
app.register_blueprint(contribute_bp)


<<<<<<< HEAD
@app.route('/')
def hello():
    return render_template('contribute/home.html')

=======
# @app.route('/')
# def hello():
#     return render_template('contribute/home.html')

authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
request_url = 'https://api.github.com'
client_id = os.getenv("CLIENT_ID", "SECRET_KEY")
client_secret = os.getenv("CLIENT_SECRET", "SECRET_KEY")
# 1. Shows login page with a random 'state' parameter to prevent CSRF

@app.route('/')
def showLogin():
  '''
    Shows login page. Sends a random 'state' parameter to the page
    to prevent csrf. 
    The value of 'state' is also stored in session object for future use.
    Returns a random string for 'state' and an optional template.
  '''
  state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
  login_session['state'] = state
  print(login_session)
  # return jsonify(state=state) # to return state in a json response
  return render_template('contribute/home.html', state=state)
  # return redirect()


@app.route('/handleLogin', methods=["GET"])
def handleLogin():
    '''
      This method makes initial request to get authorization
      permissions from the user. It has the following parameters:
      1. client_id: create one at - https://github.com/settings/applications/new
      2. state: Random string used to prevent CSRF
      3. scope: scope of permissions
      You will setup a Authorization Callback URL when you create your new application on
      Github. If the request is successfull Github redirects to that URL with a 'code'
      parameter.
      Requests temporary 'code' value from Github.
    '''
    # if login_session['state'] == request.args.get('state'):
        # print login_session['state']
    fetch_url = authorization_base_url + \
                '?client_id=' + client_id + \
                '&state=' + login_session['state'] + \
                '&scope=user%20repo%20public_repo' + \
                '&allow_signup=true'
    # print fetch_url
    return redirect(fetch_url)
    # else:
    #     print("login_session's state:", login_session['state'])
    #     print("requests.arg:", request.args)
    #     return jsonify(invalid_state_token="invalid_state_token")

#2. Using the /callback route to handle authentication.
@app.route('/callback', methods=['GET', 'POST'])
def handle_callback():
    '''
        This function helps exchange temporary 'code' value with a permanent
        access_token.
    '''
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter!'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if 'code' in request.args:
        #return jsonify(code=request.args.get('code'))
        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': request.args['code']
        }
        headers = {'Accept': 'application/json'}
        req = requests.post(token_url, params=payload, headers=headers)
        resp = req.json()

        if 'access_token' in resp:
            login_session['access_token'] = resp['access_token']
            return jsonify(access_token=resp['access_token'])
            #return redirect(url_for('index'))
        else:
            return jsonify(error="Error retrieving access_token"), 404
    else:
        return jsonify(error="404_no_code"), 404

# 3. Get user information from Github
@app.route('/index')
def index():
    # Check for access_token in session
    if 'access_token' not in login_session:
        return 'Never trust strangers', 404
    # Get user information from github api
    access_token_url = 'https://api.github.com/user?access_token={}'
    r = requests.get(access_token_url.format(login_session['access_token']))
    try:
        resp = r.json()
        gh_profile = resp['html_url']
        username = resp['login']
        avatar_url = resp['avatar_url']
        bio = resp['bio']
        name = resp['name']
        return jsonify(
          gh_profile=gh_profile,
          gh_username=username,
          avatar_url=avatar_url,
          gh_bio=bio,
          name=name
        )
    except AttributeError:
        app.logger.debug('error getting username from github, oops')
        return "something is wrong...oof", 500
>>>>>>> task/580-contribution-catalog-auth

if __name__ == '__main__':
    app.run(port=5050, host=None, debug=True)
