import logging

import connexion
from time import gmtime

from controllers.config import API_LOC
#import .controllers.config as cfg
from rokwireresolver import RokwireResolver

debug = True

log = logging.getLogger('werkzeug')
log.disabled = True

logging.Formatter.converter = gmtime
log_format = '%(asctime)-15s.%(msecs)03dZ %(levelname)-7s [%(threadName)-10s] : %(name)s - %(message)s'

if debug:
    logging.basicConfig(datefmt='%Y-%m-%dT%H:%M:%S', format=log_format, level=logging.DEBUG)
else:
    logging.basicConfig(datefmt='%Y-%m-%dT%H:%M:%S', format=log_format, level=logging.INFO)

app = connexion.FlaskApp(__name__, debug=debug, specification_dir=API_LOC)
app.add_api('rokwire.yaml', arguments={'title': 'Rokwire'}, resolver=RokwireResolver('controllers'),
            resolver_error=501)

if __name__ == '__main__':
    app.run(port=5000, host=None, server='flask', debug=debug)
