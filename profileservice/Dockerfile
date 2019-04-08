FROM python:3.6-alpine
MAINTAINER Yong Wook Kim <ywkim@illinois.edu>

#RUN apt-get update \
#  && apt-get install -y python3-pip python3-dev \
#  && cd /usr/local/bin \
#  && ln -s /usr/bin/python3 python \
#  && pip3 install --upgrade pip

WORKDIR /home/clowder

# copy requirements file
COPY requirements.txt /home/clowder/

RUN pip install -r /home/clowder/requirements.txt

# add bash
RUN apk add --no-cache bash curl

# Setup environment variables. These are passed into the container. You can change
# these to your setup. If RABBITMQ_URI is not set, it will try and use the rabbitmq
# server that is linked into the container. MAIN_SCRIPT is set to the script to be
# executed by entrypoint.sh
ENV MONGODB_URI="" \
    DB_DBNAME="clowder" \
    DB_COLLECTION="%2F" \
    MAIN_SCRIPT="rest_service.py"

# copy rest of the files needed
COPY entrypoint.sh *.py /home/clowder/
CMD python /home/clowder/rest_service.py
