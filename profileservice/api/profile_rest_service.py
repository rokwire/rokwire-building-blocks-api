import connexion
import logging
import controllers.configs as cfg

from time import gmtime
from rokwireresolver import RokwireResolver

debug = cfg.DEBUG

log = logging.getLogger('werkzeug')
log.disabled = True

logging.Formatter.converter = gmtime
log_format ='%(asctime)-15s.%(msecs)03dZ %(levelname)-7s [%(threadName)-10s] : %(name)s - %(message)s'

if debug:
    logging.basicConfig(datefmt='%Y-%m-%dT%H:%M:%S', format=log_format, level=logging.DEBUG)
else:
    logging.basicConfig(datefmt='%Y-%m-%dT%H:%M:%S', format=log_format, level=logging.INFO)

app = connexion.FlaskApp(__name__, debug=debug, specification_dir=cfg.API_LOC)
app.add_api('rokwire.yaml', base_path=cfg.PROFILE_URL_PREFIX, arguments={'title': 'Rokwire'}, resolver=RokwireResolver('controllers'),
            resolver_error=501)

if __name__ == '__main__':
    app.run(port=5000, host=None, server='flask', debug=debug)