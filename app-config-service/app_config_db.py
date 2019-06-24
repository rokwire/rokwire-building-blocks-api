from flask import current_app, g
from pymongo import MongoClient

class AppConfigDBConnection:
    
    def get_dbclient(self):
        if 'db' not in g:
            g.client = MongoClient(current_app.config['APP_CONFIG_MONGO_URL'])
            g.db = g.client.get_database(name=current_app.config['APP_CONFIG_DB_NAME'])
        return g.db
    
    
    def close_conn(self, e=None):
        client = g.pop('client', None)
    
        if client is not None:
            client.close()
    
    
    def init_app(self, app):
        app.teardown_appcontext(self.close_conn)