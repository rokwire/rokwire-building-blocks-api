import connexion

from api.controllers import config as cfg
from api.rokwireresolver import RokwireResolver

debug = cfg.DEBUG

app = connexion.FlaskApp(__name__, debug=debug, specification_dir=cfg.API_LOC)
app.add_api('rokwire.yaml', arguments={'title': 'Rokwire'}, resolver=RokwireResolver('controllers'),
            resolver_error=501)


def apikey_auth(token, required_scopes):
    # info = TOKEN_DB.get(token, None)
    #
    # if not info:
    #     raise OAuthProblem('Invalid token')
    info = "test"

    return info


if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0", server='flask', debug=debug)
