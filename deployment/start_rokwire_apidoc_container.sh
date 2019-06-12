# Start Swagger docker container to host Rokwire API documentation
sudo apt-get update
if [ -x "$(command -v docker)" ]; then
    echo "Update Docker"
    sudo apt-get --only-upgrade install docker.io
else
    echo "Install docker"
    #install Docker from Ubuntu repository
    sudo apt-get install docker.io
fi

name="rokwire-api-doc"

swaggerImage="swaggerapi/swagger-ui:latest"

matchingImage=$(sudo docker images -q $swaggerImage -q | xargs)
if [ -z $matchingImage ]; then
  echo "Pull Swagger docker image"
  sudo docker pull swaggerapi/swagger-ui
fi

matchingStarted=$(sudo docker ps --filter="name=$name" -q | xargs)
if [ -z $matchingStarted ]; then 
    matchingContainer=$(sudo docker container ls -a --filter="name=$name" -q | xargs)
    if [ ! -z $matchingContainer ]; then
        echo "Remove Swagger docker container"
        sudo docker rm $matchingContainer
    fi
    echo "Start Swagger docker container"
    sudo docker run \
        --name=$name \
        -p 80:8080 -p 8080:8080 \
        -e BASE_URL=/api/docs \
        -e SWAGGER_JSON=/rokwire-api-doc/rokwire.yaml \
        -v /home/ubuntu/ws/rokwire-building-blocks-api:/rokwire-api-doc \
        swaggerapi/swagger-ui&
fi
