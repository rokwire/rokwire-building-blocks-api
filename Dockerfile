FROM swaggerapi/swagger-ui:v3.28.0

COPY rokwire.yaml /usr/share/nginx/html/app/

ENV URLS "[{ url: 'app/rokwire.yaml', name: 'rokwire' } , { url: 'https://api-dev.rokwire.illinois.edu/health/doc', name: 'Health Building Block' } ]"

VOLUME /usr/share/nginx/html/app/

ENV BASE_URL="/docs"

CMD ["sh", "/usr/share/nginx/run.sh"]
