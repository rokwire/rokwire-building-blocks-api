# Profile Building Block

**profile rest service** is a Python project to provide rest service for rokwire building block profile
results.
                      

### Prerequisites

**MongoDB**

- A system must have a mongodb installed.

**[Python 3.5+](https://www.python.org)**


## Set Up

**MongoDB**
 
 MongoDB should be installed

**Configuration**

The necessary configuration should be configured in configure file (configs.py) that is located under profileservice folder. This contains the MongoDB url, database name, collection name and so on. Modify the information in the file appropriately.

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

## Run application

### Run locally without Docker

This service uses the python Flask and PyMongo library.

The configuration file configs.py should have the appropriate information

To install and run the location-model service, do the following:

```
cd profileservice
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python api/profile_rest_service.py`
```

If you want to use gunicorn, cd into api folder then, use ` gunicorn profile_rest_service:app -c gunicorn.config.py` instead of `python api/profile_rest_service.py` 

The profile building block should be running at http://localhost:5000
The detailed API information is in rokwire.yaml in the OpenAPI Spec 3.0 format.

### Docker Instructions
```
cd rokwire-building-blocks-api
docker build -f profileservice/Dockerfile -t rokwire/profile-building-block .
docker run --name profile --rm --env-file=profileservice/.env -e PROFILE_ENDPOINT=/profiles -e MONGO_PROFILE_URL=mongodb://<mongodb-url>:27017 -e MONGO_PII_URL=mongodb://<mongodb-url>:27017 -p 5000:5000 rokwire/profile-building-block
```

### AWS ECR Instructions

Make sure the repository called rokwire/profileservice exists in ECR. Then create Docker image for Rokwire Platform API and push to AWS ECR for deployment.

```
cd rokwire-building-blocks-api 
docker build -f profileservice/Dockerfile -t rokwire/profile-building-block .
docker tag rokwire/profile-building-block:latest 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/profileservice:latest
$(aws ecr get-login --no-include-email --region us-east-2)
docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/profileservice:latest
```

## Sample profile building block process for non-pii
The examples use 'curl' command to implement rest method to an end point `http://localhost:5000/profiles`.
### POST non-pii data for creating uuid:
The app will post without any information to the endpoint (This will happen when the app installed in the device for the first time)
```
curl  -X POST http://localhost:5000/profiles
```
API will return newly created UUID
```
{
"uuid": "a6856b73-d453-4515-8002-56e8d0522136",
"message": "new profile with new uuid has been created: a6856b73-d453-4515-8002-56e8d0522136"
}
```
### PUT non-pii data information for the existing uuid
To update the information about the non-pii dataset, this method should be used
```
curl -X PUT -d `{
              "over13": true,
              "interests": [
                    {
                        "category": "Athletics",
                        "subcategories": [
                            "Football",
                            "Basketball"
                        ]
                    },
                    {
                        "category": "Entertainment"
                    }
                ],
              "positiveInterestTags": [
                    "jazz",
                    "rock"
                ],
              "negativeInterestTags": [
                    "Rock",
                    "Hip Hop"
                ],
              "favorites": {
                  "eventIds": [],
                  "placeIds": [],
                  "diningPlaceIds": [],
                  "laundryPlaceIds": [],
                  "athleticEventIds": []
              },
              "privacySettings": {
                 "level": 1,
                 "dateModified": "2019-06-01T10:15:23Z"
              },
            }' -H "Content-Type: application/json" http://localhost:5000/profiles/a6856b73-d453-4515-8002-56e8d0522136
```
API will return update non-pii dataset
```
{
    "over13": true,
    "uuid": "a6856b73-d453-4515-8002-56e8d0522136",
    "interests":[
        {
            "subcategories":[
                "Football",
                "Basketball"
            ],
            "category": "Athletics"
        },
        {
            "category": "Entertainment"
        }
    ],
    "positiveInterestTags":[
        "jazz",
        "rock"
    ],
    "negativeInterestTags":[
        "Rock",
        "Hip Hop"
    ],
    "creationDate": "2019/07/03T11:31:44",
    "lastModifiedDate": "2019/07/03T11:37:39",
    "favorites":{
        "placeIds":[],
        "eventIds":[],
        "athleticEventIds":[],
        "laundryPlaceIds":[],
        "diningPlaceIds":[]
    }
}
```
### GET information about the existing uuid
To get the information about the existing non-pii dataset, this method should be used
```
curl http://localhost:5000/profiles/a6856b73-d453-4515-8002-56e8d0522136
```
API will return the information of the non-pii dataset
```
{
    "over13": true,
    "uuid": "a6856b73-d453-4515-8002-56e8d0522136",
    "interests":[
        {
            "subcategories":[
                "Football",
                "Basketball"
            ],
            "category": "Athletics"
        },
        {
            "category": "Entertainment"
        }
    ],
    "positiveInterestTags":[
        "jazz",
        "rock"
    ],
    "negativeInterestTags":[
        "Rock",
        "Hip Hop"
    ],
    "creationDate": "2019/07/03T11:31:44",
    "lastModifiedDate": "2019/07/03T11:37:39",
    "favorites":{
        "placeIds":[],
        "eventIds":[],
        "athleticEventIds":[],
        "laundryPlaceIds":[],
        "diningPlaceIds":[]
    }
}
```
### DELETE existing non-pii dataset
Deletion of the existing non-pii dataset
```
curl -X DELETE http://localhost:5000/profiles/a6856b73-d453-4515-8002-56e8d0522136
```
API will return the message
```
{
"message": "Object is deleted with id of : a6856b73-d453-4515-8002-56e8d0522136"
}
```

## Sample profile building block process for pii
### POST pii to create a new pii dataset:
This is for creating a new PII dataset. This will happend when the user login to the app for the first time. Input json should contain uuid and at least one unique identifier either email or phone number.
```
curl -X POST -d `{
              "uuid": "a6856b73-d453-4515-8002-56e8d0522136",
              "phone": "123-456-7890",
            }' -H "Content-Type: application/json" http://localhost:5000/profiles/pii
```
API will return newly created pii dataset
```
{
    "message": "Pii data has been posted with : 90e7b9ee-de9c-4e2e-a32a-0295e92b035b",
    "pid": "90e7b9ee-de9c-4e2e-a32a-0295e92b035b"
}
```
### PUT pii information to update pii dataset:
This method is for updateing the information of the existing pii
```
curl -X PUT -d `{
              "uuid": ["a6856b73-d453-4515-8002-56e8d0522136"],
              "lastname": "doe",
              "firstname": "john",
              "phone": "123-456-7890",
              "email": "jd@testmail.com",
              "username": "jd325",
              "uin": "2340345",
              "netid": "jd123"
            }' -H "Content-Type: application/json" http://localhost:5000/profiles/pii/90e7b9ee-de9c-4e2e-a32a-0295e92b035b
```
API will return update non-pii dataset
```
{
    "lastModifiedDate": "2019/07/03T11:53:12",
    "netid": "jd123",
    "uin": "2340345",
    "firstname": "john",
    "pid": "90e7b9ee-de9c-4e2e-a32a-0295e92b035b",
    "imageUrl": null,
    "email": "jd@testmail.com",
    "username": "jd325",
    "creationDate": "2019/07/03T11:51:43",
    "lastname": "doe",
    "phone": "123-456-7890",
    "uuid":[
        "a6856b73-d453-4515-8002-56e8d0522136"
    ]
}
```
### GET pii information of the existing pii dataset:
This method is for obtaining the information of the existing pii
```
curl http://localhost:5000/profiles/pii/90e7b9ee-de9c-4e2e-a32a-0295e92b035b
```
API will return update non-pii dataset
```
{
    "lastModifiedDate": "2019/07/03T11:53:12",
    "netid": "jd123",
    "uin": "2340345",
    "firstname": "john",
    "pid": "90e7b9ee-de9c-4e2e-a32a-0295e92b035b",
    "imageUrl": null,
    "email": "jd@testmail.com",
    "username": "jd325",
    "creationDate": "2019/07/03T11:51:43",
    "lastname": "doe",
    "phone": "123-456-7890",
    "uuid":[
        "a6856b73-d453-4515-8002-56e8d0522136"
    ]
}
```
### DELETE existing pii dataset
Deletion of the existing non-pii dataset
```
curl -X DELETE http://localhost:5000/profiles/pii/90e7b9ee-de9c-4e2e-a32a-0295e92b035b
```
API will return the message
```
{
"message": "Object is deleted with id of : 90e7b9ee-de9c-4e2e-a32a-0295e92b035b"
}
```
