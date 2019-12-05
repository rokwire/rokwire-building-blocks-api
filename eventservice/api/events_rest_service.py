import connexion
import controllers.configs as cfg
from utils.db import init_db
from rokwireresolver import RokwireResolver

debug = cfg.DEBUG

app = connexion.FlaskApp(__name__, debug=debug, specification_dir=cfg.API_LOC)
app.add_api('rokwire.yaml', arguments={'title': 'Rokwire'}, resolver=RokwireResolver('controllers'),
            resolver_error=501)

if __name__ == '__main__':

    init_db()

    app.run(port=5000, host=None, server='flask', debug=debug)
