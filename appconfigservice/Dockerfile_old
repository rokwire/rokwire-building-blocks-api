FROM tiangolo/uwsgi-nginx:python3.6

LABEL maintainer="Xiaoxia Liao <xialiao@illinois.edu>"

ADD ./requirements.txt /code_buildtime_tmp/requirements.txt
WORKDIR /code_buildtime_tmp
RUN pip install -q -r requirements.txt

# URL under which static (not modified by Python) files will be requested
# They will be served by Nginx directly, without being handled by uWSGI
#ENV STATIC_URL /static
# Absolute path in where the static files wil be
#ENV STATIC_PATH /app/static

# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured)
# ENV STATIC_INDEX 1
ENV STATIC_INDEX 0

#customize listen port
ENV LISTEN_PORT 5000
EXPOSE 5000

# Add app config
COPY ./app /app
WORKDIR /app

#For using DocumentDB
RUN wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem

# Make /app/* available to be imported by Python globally to better support several use cases like Alembic migrations.
ENV PYTHONPATH=/app

# Move the base entrypoint to reuse it
RUN mv /entrypoint.sh /uwsgi-nginx-entrypoint.sh
# Copy the entrypoint that will generate Nginx additional configs
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Run the start script provided by the parent image tiangolo/uwsgi-nginx.
# It will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Supervisor, which in turn will start Nginx and uWSGI
CMD ["/start.sh"]