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

name="app_config"

appconfigImage="app_config:latest"

matchingImage=$(sudo docker images -q $appconfigImage -q | xargs)
if [ -z $matchingImage ]; then
  echo "Building app_config docker"
  docker build -t=app_config:latest ../appconfigservice
fi

matchingStarted=$(sudo docker ps --filter="name=$name" -q | xargs)
if [ -z $matchingStarted ]; then 
    matchingContainer=$(sudo docker container ls -a --filter="name=$name" -q | xargs)
    if [ ! -z $matchingContainer ]; then
        echo "Remove app_config docker container"
        sudo docker rm $matchingContainer
    fi
    echo "Start app_config docker container"
    sudo docker run --network host -d --name app_config -it app_config:latest&
fi
 