FROM swaggerapi/swagger-ui:v3.23.5

COPY rokwire.yaml /usr/share/nginx/html/app/

ENV URLS "[{ url: 'app/rokwire.yaml', name: 'rokwire' } , { url: 'https://api-dev.rokwire.illinois.edu/health/doc', name: 'rokwire-health' } ]"

VOLUME /usr/share/nginx/html/app/

ENV BASE_URL="/docs"

CMD ["sh", "/usr/share/nginx/run.sh"]