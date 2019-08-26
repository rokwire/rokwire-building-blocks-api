FROM swaggerapi/swagger-ui:v3.23.5

COPY rokwire.yaml /app/rokwire.yaml

ENV SWAGGER_JSON="/app/rokwire.yaml"
ENV BASE_URL="/docs"

CMD ["sh", "/usr/share/nginx/run.sh"]