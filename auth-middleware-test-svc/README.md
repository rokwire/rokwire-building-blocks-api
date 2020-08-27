# auth-middleware-test-svc

The purpose of this app is to demonstrate the usage of the new auth-middleware (`lib/auth-middleware`)

Pay attention to these things:

- requirements.txt: notice line `../lib/auth-middleware`
- docker build context changes
  - the build context for docker builds should be `rokwire-building-blocks-api`, and not the individual web service apps (eventservice, profileservice, etc.).  The reason for this is that the auth-middleware project is in `rokwire-building-blocks-api/lib/auth-middleware`, which must be within the build context
    - dir structure:
      - `rokwire-building-blocks-api` - build context
        - `auth-middleware-test-svc` - example web app for docker build. We are unable to build if this is the build context, because we can't access `rokwire-building-blocks-api/lib/` because it's outside of the build context
      - `lib`
        - `auth-middleware`
  - The Dockerfile will need be changed to allow for the fact that the build context is one level above the individual web service apps.
  - [docker build instructions here](#docker-build)
- See the readme.md file for the `lib/auth-middleware` python package for environment variables that will need to be set in your building block instance.

## Environment File

You need to have a `.env` file in this directory that contains credentials required for authentication. 
Not all of these variables may be required for this test. 

Example file format:
```
TWILIO_ACCT_SID=<Twilio Account SID>
TWILIO_AUTH_TOKEN=<Twilio Auth Token>
TWILIO_VERIFY_SERVICE_ID=<Twilio Verify Service ID>

PHONE_VERIFY_SECRET=<Phone Verify Secret> 
PHONE_VERIFY_AUDIENCE=<Phone Verify Audience>

SHIBBOLETH_HOST=<Shibboleth Host Name>
SHIBBOLETH_CLIENT_ID=<Shibboleth Client ID>
```

## Run application

### Run locally without Docker
```
cd rokwire-building-blocks-api/auth-middleware-test-svc
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python flaskapp.py`
```

If you want to use gunicorn, cd into api folder then, use ` gunicorn flaskapp:app -c gunicorn.config.py` instead of `python flaskapp.py` 

It should be running at http://localhost:5000

### Docker Instructions

```
cd rokwire-building-blocks-api
docker build -t rokwire/auth_middleware_test -f auth-middleware-test-svc/Dockerfile .
docker run --rm --env-file=auth-middleware-test-svc/.env  -p 5000:5000 rokwire/auth_middleware_test
```
