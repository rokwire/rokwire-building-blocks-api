# Logging Building Block

The goal of the Logging Building Block is to provide a set of RESTFul web services to log all the activities of the bp.
                      

## Setup Environment
```
cd loggingservice
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Environment File

You need to have a `.env` file in this directory that contains credentials required for authentication. 
Not all of these variables may be required for this building block. 

Example file format:

```
TWILIO_ACCT_SID=<Twilio Account SID>
TWILIO_AUTH_TOKEN=<Twilio Auth Token>
TWILIO_VERIFY_SERVICE_ID=<Twilio Verify Service ID>

PHONE_VERIFY_SECRET=<Phone Verify Secret> 
PHONE_VERIFY_AUDIENCE=<Phone Verify Audience>

SHIBBOLETH_HOST=<Shibboleth Host Name>
SHIBBOLETH_CLIENT_ID=<Shibboleth Client ID>

ROKWIRE_API_KEY=<Rokwire API Key>
ROKWIRE_ISSUER=<Rokwire ID Token Issuer Name>

# AWS environment variables to set when running on development machine. 
# This is not required when running within AWS.
AWS_ACCESS_KEY_ID=<AWS Access Key ID>
AWS_SECRET_ACCESS_KEY=<AWS Secret Access Key>
```

## Run in Development Mode

```
cd loggingservice
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
cp -r ../lib api/lib
python profile_rest_service.py
```
and the Logging Building Block should be running at localhost at port 5000 (http://localhost:5000/logs).
The detailed API information is in rokwire.yaml in the OpenAPI Spec 3.0 format.

## Docker Instructions
```
cd rokwire-building-blocks-api
docker build -f loggingservice/Dockerfile -t rokwire/logging-building-block .
docker run --rm --name logging --env-file loggingservice/.env -e LOGGING_URL_PREFIX=<url_prefix_starting_with_slash> -p 5000:5000 rokwire/logging-building-block
```
You can edit config.py or environment variable to specify a URL prefix.
```
LOGGING_URL_PREFIX="/logs"
```

## AWS ECR Instructions

Make sure the repository called rokwire/logging-building-block exists in ECR. Then create Docker image for Rokwire Platform API and push to AWS ECR for deployment.

```
$(aws ecr get-login --no-include-email --region us-east-2)
cd rokwire-building-blocks-api
docker build -f loggingservice/Dockerfile -t rokwire/logging-building-block .
docker tag rokwire/logging-building-block:latest 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/logging-building-block:latest
docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/logging-building-block:latest
```

## Sample Logs for Post Endpoint:

Let us use ```curl``` command to post two sample events to the Events Building Block running at `http://localhost:5000/logs`.

```
curl -d '{
            "timestamp": "2019-06-01T10:15:23Z",
            "uuid": "56fe224b-3600-4b66-ac8d-5d2906e19fc61",
            "os": "ios",
            "osVersion": "10.1.4",
            "appVersion": "1.2",
            "device": "iphone 7",
            "deviceSettings": {
                "description": "test device description",
                "setting": "test setting"
            },
            "userAction": {
                "description": "test description",
                "type": "test type",
                "name": "test name",
                "mainFeature": "test main feature",
                "subFeature": "test sub feature",
                "customAttribute1": "test custom attribute 1",
                "customAttribute2": "test custom attribute 2",
                "customAttribute3": "test custom attribute 3",
                "customAttribute4": "test custom attribute 4",
                "customAttribute5": "test custom attribute 5"
            }
}' -H "Content-Type: application/json" -X POST http://localhost:5000/logs
```

It will return back the `post` status in json which includes the internal id as below:

```
{
    message": "[POST]: logging record posted: uuid = 56fe224b-3600-4b66-ac8d-5d2906e19fc61",
    "status": 201,
    "uuid": "56fe224b-3600-4b66-ac8d-5d2906e19fc61"
}
```


