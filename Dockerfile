FROM swaggerapi/swagger-ui:v3.28.0

COPY appconfigservice/appconfig.yaml /usr/share/nginx/html/app/
COPY authservice/auth.yaml /usr/share/nginx/html/app/
COPY eventservice/events.yaml /usr/share/nginx/html/app/
COPY profileservice/profile.yaml /usr/share/nginx/html/app/
COPY loggingservice/logging.yaml /usr/share/nginx/html/app/

ENV URLS "[{url: 'app/appconfig.yaml', name: 'App Config Building Block'}, {url: 'app/auth.yaml', name: 'Authentication Building Block'}, {url: 'app/events.yaml', name: 'Events Building Block'}, {url: 'app/profile.yaml', name: 'Profile Building Block'}, {url: 'app/logging.yaml', name: 'Logging Building Block'}, {url: 'https://api-dev.rokwire.illinois.edu/health/doc', name: 'Health Building Block'} ]"

VOLUME /usr/share/nginx/html/app/

ENV BASE_URL="/docs"

CMD ["sh", "/usr/share/nginx/run.sh"]
