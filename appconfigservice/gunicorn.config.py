"""Gunicorn configuration."""

bind = '0.0.0.0:5000'

workers = 4
worker_class = 'gevent'
# If you adjust this number, also adjust the MongoClient pool connections
worker_connections = 100
