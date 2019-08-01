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

## run

- make present-working-directory this one (`rokwire-building-blocks-api/auth-middleware-test-svc/`)
- execute run command
  - docker compose
    - `$ docker-compose up`
  - standard python (need to pip install requirements, and recommend using a virtualenv)
    - `$ python flaskapp.py`

## docker build

### std docker

- make present-working-directory the parent directory
  - eg.
    - this project = `rokwire-building-blocks-api/auth-middleware-test-svc`
    - parent directory = `rokwire-building-blocks-api` - build context
- `$ docker build -f auth-middleware-test-svc/Dockerfile .`

### docker compose

- make present-working-directory this one (`rokwire-building-blocks-api/auth-middleware-test-svc/`)
- `$ docker-compose build`
