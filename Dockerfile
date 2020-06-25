FROM swaggerapi/swagger-ui:v3.23.5

COPY rokwire.yaml /usr/share/nginx/html/app/

#TODO change health url
ENV URLS "[{ url: 'app/rokwire.yaml', name: 'rokwire' } , { url: 'http://petstore.swagger.io/v2/swagger.json', name: 'rokwire-health' } ]"

VOLUME /usr/share/nginx/html/app/

ENV BASE_URL="/docs"

CMD ["sh", "/usr/share/nginx/run.sh"]