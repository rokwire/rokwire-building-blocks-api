# Contributions Building Block

Contributions Building Block provides a set of RESTFul web services to manage Contributions in the Rokwire platform. This includes adding a new contribution (a combination of Talents and Capabilities), retrieving relevant contributions based on search query, updating and deleting existing contributions, etc.
                      

### Prerequisites

**MongoDB**

- A system must have a mongodb installed.

**[Python 3.5+](https://www.python.org)**


## Set Up

**MongoDB**
 
 MongoDB should be installed

**Configuration**

The necessary configuration should be configured in configure file (configs.py) that is located under contributions folder. This contains the MongoDB url, database name, collection name and so on. Modify the information in the file appropriately.

## Environment File

You need to have a `.env` file in this directory that contains credentials required for authentication. 
Not all of these variables may be required for this building block. 

Example file format:

```
ROKWIRE_API_KEY=<Rokwire API Key>   # pragma: allowlist secret
ROKWIRE_ISSUER=<Rokwire ID Token Issuer Name>   # pragma: allowlist secret

# AWS environment variables to set when running on development machine. 
# This is not required when running within AWS.
AWS_ACCESS_KEY_ID=<AWS Access Key ID>   # pragma: allowlist secret
AWS_SECRET_ACCESS_KEY=<AWS Secret Access Key>   # pragma: allowlist secret
```

## Run application

### Run locally without Docker

This service uses the python Flask and PyMongo library.

The configuration file configs.py should have the appropriate information

To install and run the location-model service, do the following:
```
cd contributions
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python api/contributions_rest_service.py
```

- (Windows):
```
cd contributions
py -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python api/contributions_rest_service.py
```

If you want to use gunicorn, cd into api folder then, use ` gunicorn contributions_rest_service:app -c gunicorn.config.py` instead of `python api/contributions_rest_service.py` 

The contributions building block should be running at http://localhost:5000
The detailed API information is in contribution.yaml in the OpenAPI Spec 3.0 format.

### Docker Instructions
```
cd rokwire-building-blocks-api
docker build -f contributions/Dockerfile -t rokwire/contributions-building-block .
docker run --name contribution --rm --env-file=contributions/.env -e CONTRIBUTION_URL_PREFIX=<url_prefix_starting_with_slash> -e MONGO_CONTRIBUTION_URL=mongodb://<mongodb-url>:27017 -p 5000:5000 rokwire/contributions-building-block
```
You can edit config.py or environment variable to specify a URL prefix by modifying CONTRIBUTION_URL_PREFIX variable.
If you need to make just /contributions as endpoint, put the vaiable value to empty string or do not include this variable.


### AWS ECR Instructions

Make sure the repository called rokwire/contributions exists in ECR. Then create Docker image for Rokwire Platform API and push to AWS ECR for deployment.

```
cd rokwire-building-blocks-api 
docker build -f contributions/Dockerfile -t rokwire/contributions-building-block .
docker tag rokwire/contributions-building-block:latest 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/contributions:latest
$(aws ecr get-login --no-include-email --region us-east-2)
docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/contributions:latest
```

## Sample contributions building block process
The examples use 'curl' command to implement rest method to an end point `http://localhost:5000/contributions`.
### POST contributions data for creating contribution entry and id:
The app will post with given information to the endpoint
```
curl -X POST -d `{
                   "shortDescription":"Short description of the contribution",
                   "name":"test",
                   "contributionAdmins": [
                       "adminuser"
                   ],
                   "talents":null,
                   "capabilities":[
                      {
                         "apiDocUrl":null,
                         "healthCheckUrl":"healthCheckUrl",
                         "deploymentDetails":{
                            "authMethod":null,
                            "databaseDetails":null,
                            "environmentVariables":null,
                            "location":"internal"
                         },
                         "version":"version",
                         "description":"capability description",
                         "isOpenSource":true,
                         "name":"capability test",
                         "apiBaseUrl":null,
                         "dataDeletionEndpointDetails":{
                            "apiKey":"apiKey",  # pragma: allowlist secret
                            "description":"description",
                            "deletionEndpoint":"deletionEndpoint"
                         },
                         "status":"Submitted"
                      }
                   ],
                   "longDescription":null,
                   "contributors":[
                      {
                         "firstName":null,
                         "lastName":null,
                         "email":null,
                         "phone":null,
                         "affiliation":{
                            "name":null,
                            "address":null,
                            "phone":null,
                            "email":null
                         }
                      }
                   ]
                }' -H "Content-Type: application/json" http://localhost:5000/contributions
```
API will return newly created ID
```
{
"id": "5ed9440f830d3038f4f8ffaa",
"message": "new contribution has been created: test"
}
```
### PUT contribution data information for the existing id
To update the information about the non-pii dataset, this method should be used
```
curl -X PUT -d `{
                   "shortDescription":"Short description of the contribution",
                   "name":"test1",
                   "contributionAdmins": [
                       "adminuser"
                   ],
                   "talents":[
                       {
                          "name":"talent 1",
                          "shortDescription":"short description",
                          "requiredCapabilities":[
                             {
                                "apiDocUrl":null,
                                "healthCheckUrl":"healthCheckUrl",
                                "deploymentDetails":{
                                   "authMethod":null,
                                   "databaseDetails":null,
                                   "environmentVariables":null,
                                   "location":"internal"
                                },
                                "version":"version",
                                "description":"capability description",
                                "isOpenSource":true,
                                "name":"capability test",
                                "apiBaseUrl":null,
                                "dataDeletionEndpointDetails":{
                                   "apiKey":"apiKey",   # pragma: allowlist secret
                                   "description":"description",
                                   "deletionEndpoint":"deletionEndpoint"
                                },
                                "status":"Submitted"
                             },
                             {
                                "apiDocUrl":null,
                                "healthCheckUrl":"healthCheckUrl",
                                "deploymentDetails":{
                                   "authMethod":null,
                                   "databaseDetails":null,
                                   "environmentVariables":null,
                                   "location":"internal"
                                },
                                "version":"version",
                                "description":"capability2 description",
                                "isOpenSource":true,
                                "name":"capability2 test",
                                "apiBaseUrl":null,
                                "dataDeletionEndpointDetails":{
                                   "apiKey":"apiKey",   # pragma: allowlist secret
                                   "description":"description",
                                   "deletionEndpoint":"deletionEndpoint"
                                },
                                "status":"Submitted"
                             }
                          ],
                          "minUserPrivacyLevel":5,
                          "requiredBuildingBlocks":[
                             "App Config",
                             "Talent Chooser"
                          ],
                          "minEndUserRoles":[
                             "alumni",
                             "employee"
                          ],
                          "startDate":"2020/06/15T12:06:55",
                          "endDate":"2020/10/25T12:06:55",
                          "dataDescription":"Data description",
                          "selfCertification":{
                             "dataDeletionUponRequest":"data deletion upon request",
                             "discloseAds":"disclose ads"
                          }
                       }
                    ],
                   "capabilities":[
                      {
                         "apiDocUrl":null,
                         "healthCheckUrl":"healthCheckUrl",
                         "deploymentDetails":{
                            "authMethod":"auth method",
                            "databaseDetails":null,
                            "environmentVariables":null,
                            "location":"internal"
                         },
                         "name":"capability test1",
                         "dataDeletionEndpointDetails":{
                            "apiKey":"apiKey",  # pragma: allowlist secret
                            "description":"description",
                            "deletionEndpoint":"deletionEndpoint"
                         },
                         "isOpenSource":true,
                         "version":"version",
                         "description":"capability description",
                         "status":"Submitted",
                         "apiBaseUrl":null,
                         "contacts":[
                            {
                               "phone":"phone",
                               "name":null,
                               "officialAddress":null,
                               "email":null,
                               "organization":null
                            },
                            {
                               "phone":"phone 2",
                               "name":"name 2",
                               "officialAddress":null,
                               "email":null,
                               "organization":null
                            }
                         ]
                      },
                      {
                         "apiDocUrl":null,
                         "healthCheckUrl":"healthCheckUrl",
                         "deploymentDetails":{
                            "authMethod":"auth method",
                            "databaseDetails":null,
                            "environmentVariables":null,
                            "location":"internal"
                         },
                         "name":"capability test2",
                         "dataDeletionEndpointDetails":{
                            "apiKey":"apiKey",  # pragma: allowlist secret
                            "description":"description",
                            "deletionEndpoint":"deletionEndpoint"
                         },
                         "isOpenSource":true,
                         "version":"version",
                         "description":"capability description",
                         "status":"Submitted",
                         "apiBaseUrl":null,
                         "contacts":[
                            {
                               "phone":"phone",
                               "name":null,
                               "officialAddress":null,
                               "email":null,
                               "organization":null
                            },
                            {
                               "phone":"phone 2",
                               "name":"name 2",
                               "officialAddress":null,
                               "email":null,
                               "organization":null
                            }
                         ]
                      }
                   ],
                   "longDescription":null,
                   "contributors":[
                      {
                         "firstName":"frist name",
                         "email":null,
                         "phone":null,
                         "affiliation":{
                            "name":"test affilication",
                            "address":null,
                            "phone":null,
                            "email":null
                         }
                      },
                      {
                         "name":"name",
                         "address":null,
                         "phone":null
                      }
                   ]
                }' -H "Content-Type: application/json" http://localhost:5000/contributions/5ed9440f830d3038f4f8ffaa
```
API will return updated contribution dataset
```
    {
       "contributors":[
          {
             "firstName":"frist name",
             "email":null,
             "affiliation":{
                "email":null,
                "phone":null,
                "address":null,
                "name":"test affilication"
             },
             "phone":null
          },
          {
             "name":"name",
             "phone":null,
             "address":null
          }
       ],
       "id": "5ed9440f830d3038f4f8ffaa",
       "shortDescription":"Short description of the contribution",
       "capabilities":[
          {
             "deploymentDetails":{
                "databaseDetails":null,
                "authMethod":null,
                "dockerImageName":null,
                "location":null,
                "environmentVariables":"null…"
             },
             "description":"capability description",
             "name":"capability test1",
             "isOpenSource":true,
             "dataDeletionEndpointDetails":{
                "apiKey":"apiKey",  # pragma: allowlist secret
                "deletionEndpoint":"deletionEndpoint",
                "description":"description"
             },
             "status":"Submitted",
             "apiDocUrl":null,
             "contacts":[
                {
                   "email":null,
                   "organization":null,
                   "phone":null,
                   "officialAddress":null,
                   "name":null
                },
                {
                   "email":null,
                   "organization":null,
                   "phone":null,
                   "officialAddress":null,
                   "name":null
                }
             ],
             "healthCheckUrl":"healthCheckUrl",
             "version":"version",
             "apiBaseUrl":null
          },
          {
             "deploymentDetails":{
                "databaseDetails":null,
                "authMethod":null,
                "dockerImageName":null,
                "location":null,
                "environmentVariables":null
             },
             "description":"capability description",
             "name":"capability test2",
             "isOpenSource":true,
             "dataDeletionEndpointDetails":{
                "apiKey":"apiKey",  # pragma: allowlist secret
                "deletionEndpoint":"deletionEndpoint",
                "description":"description"
             },
             "status":"Submitted",
             "apiDocUrl":null,
             "contacts":[
                {
                   "email":null,
                   "organization":null,
                   "phone":null,
                   "officialAddress":null,
                   "name":null
                },
                {
                   "email":null,
                   "organization":null,
                   "phone":null,
                   "officialAddress":null,
                   "name":null
                }
             ],
             "healthCheckUrl":"healthCheckUrl",
             "version":"version",
             "apiBaseUrl":null
          }
       ],
       "dateModified":"2020/06/04T14:02:49",
       "longDescription":null,
       "name":"test1",
       "contributionAdmins": [
            "adminuser"
        ],
       "talents":[
           {
              "name":"talent 1",
              "shortDescription":"short description",
              "requiredCapabilities":[
                 {
                    "apiDocUrl":null,
                    "healthCheckUrl":"healthCheckUrl",
                    "deploymentDetails":{
                       "authMethod":null,
                       "databaseDetails":null,
                       "environmentVariables":null,
                       "location":"internal"
                    },
                    "version":"version",
                    "description":"capability description",
                    "isOpenSource":true,
                    "name":"capability test",
                    "apiBaseUrl":null,
                    "dataDeletionEndpointDetails":{
                       "apiKey":"apiKey",   # pragma: allowlist secret
                       "description":"description",
                       "deletionEndpoint":"deletionEndpoint"
                    },
                    "status":"Submitted"
                 },
                 {
                    "apiDocUrl":null,
                    "healthCheckUrl":"healthCheckUrl",
                    "deploymentDetails":{
                       "authMethod":null,
                       "databaseDetails":null,
                       "environmentVariables":null,
                       "location":"internal"
                    },
                    "version":"version",
                    "description":"capability2 description",
                    "isOpenSource":true,
                    "name":"capability2 test",
                    "apiBaseUrl":null,
                    "dataDeletionEndpointDetails":{
                       "apiKey":"apiKey",   # pragma: allowlist secret
                       "description":"description",
                       "deletionEndpoint":"deletionEndpoint"
                    },
                    "status":"Submitted"
                 }
              ],
              "minUserPrivacyLevel":5,
              "requiredBuildingBlocks":[
                 "App Config",
                 "Talent Chooser"
              ],
              "minEndUserRoles":[
                 "alumni",
                 "employee"
              ],
              "startDate":"2020/06/15T12:06:55",
              "endDate":"2020/10/25T12:06:55",
              "dataDescription":"Data description",
              "selfCertification":{
                 "dataDeletionUponRequest":"data deletion upon request",
                 "discloseAds":"disclose ads"
              }
           }
        ],
       "dateCreated":"2020/06/04T13:57:14"
    }
```
### GET information about the existing contribution data using id
To get the information about the existing non-pii dataset, this method should be used
```
curl http://localhost:5000/contributions/5ed9440f830d3038f4f8ffaa
```
API will return the information of the contribution dataset
```
    {
       "contributors":[
          {
             "firstName":"frist name",
             "email":null,
             "affiliation":{
                "email":null,
                "phone":null,
                "address":null,
                "name":"test affilication"
             },
             "phone":null
          },
          {
             "name":"name",
             "phone":null,
             "address":null
          }
       ],
       "id": "5ed9440f830d3038f4f8ffaa",
       "shortDescription":"Short description of the contribution",
       "capabilities":[
          {
             "deploymentDetails":{
                "databaseDetails":null,
                "authMethod":null,
                "dockerImageName":null,
                "location":null,
                "environmentVariables":null
             },
             "apiBaseUrl":null,
             "id":"3b372942-a6af-4ac6-b540-33bb36afb657",
             "description":"capability description",
             "dataDeletionEndpointDetails":{
                "apiKey":"apiKey",  # pragma: allowlist secret
                "deletionEndpoint":"deletionEndpoint",
                "description":"description"
             },
             "contacts":[
                {
                   "email":null,
                   "organization":null,
                   "phone":null,
                   "name":null,
                   "officialAddress":null
                },
                {
                   "email":null,
                   "organization":null,
                   "phone":null,
                   "name":null,
                   "officialAddress":null
                }
             ],
             "name":"capability test1",
             "apiDocUrl":null,
             "isOpenSource":true,
             "healthCheckUrl":"healthCheckUrl",
             "version":"version"
          },
          {
             "deploymentDetails":{
                "databaseDetails":null,
                "authMethod":null,
                "dockerImageName":null,
                "location":null,
                "environmentVariables":null
             },
             "apiBaseUrl":null,
             "id":"6ac72942-a6af-4ac6-b540-33bb36afb342",
             "description":"capability description",
             "dataDeletionEndpointDetails":{
                "apiKey":"apiKey",  # pragma: allowlist secret
                "deletionEndpoint":"deletionEndpoint",
                "description":"description"
             },
             "contacts":[
                {
                   "email":null,
                   "organization":null,
                   "phone":null,
                   "name":null,
                   "officialAddress":null
                },
                {
                   "email":null,
                   "organization":null,
                   "phone":null,
                   "name":null,
                   "officialAddress":null
                }
             ],
             "name":"capability test2",
             "apiDocUrl":null,
             "isOpenSource":true,
             "healthCheckUrl":"healthCheckUrl",
             "version":"version"
          }
       ],
       "status":"Submitted",
       "dateModified":"2020/06/04T14:02:49",
       "longDescription":null,
       "name":"test1",
       "contributionAdmins": [
            "adminuser"
       ],
       "talents":[
           {
              "name":"talent 1",
              "shortDescription":"short description",
              "id":"412a2942-a6af-4ac6-b540-33bb36afaf23",
              "requiredCapabilities":[
                 {
                    "apiDocUrl":null,
                    "healthCheckUrl":"healthCheckUrl",
                    "id":"61da2942-a6af-4ac6-b540-33bb36af841a",
                    "deploymentDetails":{
                       "authMethod":null,
                       "databaseDetails":null,
                       "environmentVariables":null,
                       "location":"internal"
                    },
                    "version":"version",
                    "description":"capability description",
                    "isOpenSource":true,
                    "name":"capability test",
                    "apiBaseUrl":null,
                    "dataDeletionEndpointDetails":{
                       "apiKey":"apiKey",   # pragma: allowlist secret
                       "description":"description",
                       "deletionEndpoint":"deletionEndpoint"
                    },
                    "status":"Submitted"
                 },
                 {
                    "apiDocUrl":null,
                    "healthCheckUrl":"healthCheckUrl",
                    "id":"6bc72942-a6af-4ac6-b540-33bb36afb132",
                    "deploymentDetails":{
                       "authMethod":null,
                       "databaseDetails":null,
                       "environmentVariables":null,
                       "location":"internal"
                    },
                    "version":"version",
                    "description":"capability2 description",
                    "isOpenSource":true,
                    "name":"capability2 test",
                    "apiBaseUrl":null,
                    "dataDeletionEndpointDetails":{
                       "apiKey":"apiKey",   # pragma: allowlist secret
                       "description":"description",
                       "deletionEndpoint":"deletionEndpoint"
                    }
                 }
              ],
              "minUserPrivacyLevel":5,
              "requiredBuildingBlocks":[
                 "App Config",
                 "Talent Chooser"
              ],
              "minEndUserRoles":[
                 "alumni",
                 "employee"
              ],
              "startDate":"2020/06/15T12:06:55",
              "endDate":"2020/10/25T12:06:55",
              "dataDescription":"Data description",
              "selfCertification":{
                 "dataDeletionUponRequest":"data deletion upon request",
                 "discloseAds":"disclose ads"
              }
           }
        ],
       "dateCreated":"2020/06/04T13:57:14"
    }
```
### DELETE existing contribution dataset
Deletion of the existing contribution dataset
```
curl -X DELETE http://localhost:5000/profiles/5ed9440f830d3038f4f8ffaa
```
API will return the message
```
    {
       "ID":"5ed9440f830d3038f4f8ffaa"
    }
```
### GET capabilities in contribution data using contribution id
To get the information about capabilities in certain contribution dataset, this method should be used
```
curl http://localhost:5000/contributions/5ed57231830d301a14974900/capabilities
```
API will return the information of the capabilities in contribution dataset
```
    [
       {
          "apiBaseUrl":null,
          "id":"3b372942-a6af-4ac6-b540-33bb36afb657",
          "apiDocUrl":null,
          "contacts":[
             {
                "email":null,
                "name":null,
                "officialAddress":null,
                "organization":null,
                "phone":null
             },
             {
                "email":null,
                "name":null,
                "officialAddress":null,
                "organization":null,
                "phone":null
             }
          ],
          "dataDeletionEndpointDetails":{
             "apiKey":"apiKey", # pragma: allowlist secret
             "deletionEndpoint":"deletionEndpoint",
             "description":"description"
          },
          "deploymentDetails":{
             "authMethod":null,
             "databaseDetails":null,
             "dockerImageName":null,
             "environmentVariables":null,
             "location":null
          },
          "description":"capability description",
          "healthCheckUrl":"healthCheckUrl",
          "isOpenSource":true,
          "name":"capability test1",
          "version":"version"
       },
       {
          "apiBaseUrl":null,
          "apiDocUrl":null,
          "id":"12f72942-a6af-4ac6-b540-33bb36afb341",
          "contacts":[
             {
                "email":null,
                "name":null,
                "officialAddress":null,
                "organization":null,
                "phone":null
             },
             {
                "email":null,
                "name":null,
                "officialAddress":null,
                "organization":null,
                "phone":null
             }
          ],
          "dataDeletionEndpointDetails":{
             "apiKey":"apiKey", # pragma: allowlist secret
             "deletionEndpoint":"deletionEndpoint",
             "description":"description"
          },
          "deploymentDetails":{
             "authMethod":null,
             "databaseDetails":null,
             "dockerImageName":null,
             "environmentVariables":null,
             "location":null
          },
          "description":"capability description",
          "healthCheckUrl":"healthCheckUrl",
          "isOpenSource":true,
          "name":"capability test3",
          "version":"version"
       },
       {
          "apiBaseUrl":null,
          "apiDocUrl":null,
          "id":"461a2942-a6af-4ac6-b540-33bb36af35ac",
          "contacts":[
             {
                "email":null,
                "name":null,
                "officialAddress":null,
                "organization":null,
                "phone":null
             },
             {
                "email":null,
                "name":null,
                "officialAddress":null,
                "organization":null,
                "phone":null
             }
          ],
          "dataDeletionEndpointDetails":{
             "apiKey":"apiKey", # pragma: allowlist secret
             "deletionEndpoint":"deletionEndpoint",
             "description":"description"
          },
          "deploymentDetails":{
             "authMethod":null,
             "databaseDetails":null,
             "dockerImageName":null,
             "environmentVariables":null,
             "location":null
          },
          "description":"capability description",
          "healthCheckUrl":"healthCheckUrl",
          "isOpenSource":true,
          "name":"capability test2",
          "version":"version"
       }
    ]
```
### GET capabilities in contribution data using capability name
To get the information about the capability dataset using capability name keyword, this method should be used
```
http://localhost:5000/contributions/capabilities?name=test1
```
API will return the information of the capabilities with given name
```
    [
      {
        "apiBaseUrl": null,
        "id":"3b372942-a6af-4ac6-b540-33bb36afb657",
        "apiDocUrl": null,
        "contributionId":"5ed57231830d301a14974900",
        "contacts": [
          {
            "email": null,
            "name": null,
            "officialAddress": null,
            "organization": null,
            "phone": null
          },
          {
            "email": null,
            "name": null,
            "officialAddress": null,
            "organization": null,
            "phone": null
          }
        ],
        "dataDeletionEndpointDetails": {
          "apiKey": "apiKey",   # pragma: allowlist secret
          "deletionEndpoint": "deletionEndpoint",
          "description": "description"
        },
        "deploymentDetails": {
          "authMethod": null,
          "databaseDetails": null,
          "dockerImageName": null,
          "environmentVariables": null,
          "location": null
        },
        "description": "capability description",
        "healthCheckUrl": "healthCheckUrl",
        "isOpenSource": true,
        "name": "test1",
        "version": "version"
      },
      {
        "apiBaseUrl": null,
        "id":"2af72942-a6af-4ac6-b540-33bb36afb621",
        "apiDocUrl": null,
        "contacts": null,
        "contributionId":"62a57231830d301a149bc5a3",
        "dataDeletionEndpointDetails": {
          "apiKey": "apiKey",   # pragma: allowlist secret
          "deletionEndpoint": "deletionEndpoint",
          "description": "description"
        },
        "deploymentDetails": {
          "authMethod": null,
          "databaseDetails": null,
          "dockerImageName": null,
          "environmentVariables": null,
          "location": null
        },
        "description": "capability description",
        "healthCheckUrl": "healthCheckUrl",
        "isOpenSource": true,
        "name": "test1",
        "version": "version"
      }
    ]
```
### GET talents in contribution data using contribution id
To get the information about talent in certain contribution dataset, this method should be used
```
curl http://localhost:5000/contributions/5ed57231830d301a14974900/talents
```
API will return the information of the talents in contribution dataset
```
    [
       {
          "name":"talent 1",
          "id":"3b372942-a6af-4ac6-b540-33bb36afb657",
          "shortDescription":"short description",
          "requiredCapabilities":[
             {
                "apiDocUrl":null,
                "healthCheckUrl":"healthCheckUrl",
                "deploymentDetails":{
                   "authMethod":null,
                   "databaseDetails":null,
                   "environmentVariables":null,
                   "location":"internal"
                },
                "version":"version",
                "description":"capability description",
                "isOpenSource":true,
                "name":"capability test",
                "apiBaseUrl":null,
                "dataDeletionEndpointDetails":{
                   "apiKey":"apiKey",   # pragma: allowlist secret
                   "description":"description",
                   "deletionEndpoint":"deletionEndpoint"
                }
             },
             {
                "apiDocUrl":null,
                "healthCheckUrl":"healthCheckUrl",
                "deploymentDetails":{
                   "authMethod":null,
                   "databaseDetails":null,
                   "environmentVariables":null,
                   "location":"internal"
                },
                "version":"version",
                "description":"capability2 description",
                "isOpenSource":true,
                "name":"capability2 test",
                "apiBaseUrl":null,
                "dataDeletionEndpointDetails":{
                   "apiKey":"apiKey",   # pragma: allowlist secret
                   "description":"description",
                   "deletionEndpoint":"deletionEndpoint"
                }
             }
          ],
          "minUserPrivacyLevel":5,
          "requiredBuildingBlocks":[
             "App Config",
             "Talent Chooser"
          ],
          "minEndUserRoles":[
             "alumni",
             "employee"
          ],
          "startDate":"2020/06/15T12:06:55",
          "endDate":"2020/10/25T12:06:55",
          "dataDescription":"Data description",
          "selfCertification":{
             "dataDeletionUponRequest":"data deletion upon request",
             "discloseAds":"disclose ads"
          }
       }
    ]
```
### GET talents in contribution data using talent name
To get the information about the talent dataset using talent name keyword, this method should be used
```
http://localhost:5000/contributions/talents?name=talent 1
```
API will return the information of the talents with given name
```
    [
       {
          "name":"talent 1",
          "id":"3b372942-a6af-4ac6-b540-33bb36afb657",
          "shortDescription":"short description",
          "contributionId":"5ed57231830d301a14974900",
          "requiredCapabilities":[
             {
                "apiDocUrl":null,
                "healthCheckUrl":"healthCheckUrl",
                "deploymentDetails":{
                   "authMethod":null,
                   "databaseDetails":null,
                   "environmentVariables":null,
                   "location":"internal"
                },
                "version":"version",
                "description":"capability description",
                "isOpenSource":true,
                "name":"capability test",
                "apiBaseUrl":null,
                "dataDeletionEndpointDetails":{
                   "apiKey":"apiKey",   # pragma: allowlist secret
                   "description":"description",
                   "deletionEndpoint":"deletionEndpoint"
                }
             },
             {
                "apiDocUrl":null,
                "healthCheckUrl":"healthCheckUrl",
                "deploymentDetails":{
                   "authMethod":null,
                   "databaseDetails":null,
                   "environmentVariables":null,
                   "location":"internal"
                },
                "version":"version",
                "description":"capability2 description",
                "isOpenSource":true,
                "name":"capability2 test",
                "apiBaseUrl":null,
                "dataDeletionEndpointDetails":{
                   "apiKey":"apiKey",   # pragma: allowlist secret
                   "description":"description",
                   "deletionEndpoint":"deletionEndpoint"
                }
             }
          ],
          "minUserPrivacyLevel":5,
          "requiredBuildingBlocks":[
             "App Config",
             "Talent Chooser"
          ],
          "minEndUserRoles":[
             "alumni",
             "employee"
          ],
          "startDate":"2020/06/15T12:06:55",
          "endDate":"2020/10/25T12:06:55",
          "dataDescription":"Data description",
          "selfCertification":{
             "dataDeletionUponRequest":"data deletion upon request",
             "discloseAds":"disclose ads"
          }
       }
    ]
```
### GET capabilities in contribution data using contribution id and capability id
To get the information about capabilities in certain contribution dataset 
using contribution id and capability id, this method should be used
```
curl http://localhost:5000/contributions/5ed57231830d301a14974900/capabilities/3b372942-a6af-4ac6-b540-33bb36afb657
```
API will return the information of the capabilities in contribution dataset
```
   {
      "apiBaseUrl":null,
      "apiDocUrl":null,
      "id":"3b372942-a6af-4ac6-b540-33bb36afb657",
      "contacts":[
         {
            "email":null,
            "name":null,
            "officialAddress":null,
            "organization":null,
            "phone":null
         },
         {
            "email":null,
            "name":null,
            "officialAddress":null,
            "organization":null,
            "phone":null
         }
      ],
      "dataDeletionEndpointDetails":{
         "apiKey":"apiKey", # pragma: allowlist secret
         "deletionEndpoint":"deletionEndpoint",
         "description":"description"
      },
      "deploymentDetails":{
         "authMethod":null,
         "databaseDetails":null,
         "dockerImageName":null,
         "environmentVariables":null,
         "location":null
      },
      "description":"capability description",
      "healthCheckUrl":"healthCheckUrl",
      "isOpenSource":true,
      "name":"capability test1",
      "version":"version"
   }
```
### GET talents in contribution data using contribution id and talent id
To get the information about talent in certain contribution dataset
using contribution id and talent id, this method should be used
```
curl http://localhost:5000/contributions/5ed57231830d301a14974900/talents/3b372942-a6af-4ac6-b540-33bb36afb659
```
API will return the information of the talents in contribution dataset
```
   {
      "name":"talent 1",
      "id":"3b372942-a6af-4ac6-b540-33bb36afb659",
      "shortDescription":"short description",
      "requiredCapabilities":[
         {
            "apiDocUrl":null,
            "id":"1ac72942-a6af-4ac6-b540-33bb36afb23"
            "healthCheckUrl":"healthCheckUrl",
            "deploymentDetails":{
               "authMethod":null,
               "databaseDetails":null,
               "environmentVariables":null,
               "location":"internal"
            },
            "version":"version",
            "description":"capability description",
            "isOpenSource":true,
            "name":"capability test",
            "apiBaseUrl":null,
            "dataDeletionEndpointDetails":{
               "apiKey":"apiKey",   # pragma: allowlist secret
               "description":"description",
               "deletionEndpoint":"deletionEndpoint"
            }
         },
         {
            "apiDocUrl":null,
            "id":"245b2942-a6af-4ac6-b540-33bb36afb612"
            "healthCheckUrl":"healthCheckUrl",
            "deploymentDetails":{
               "authMethod":null,
               "databaseDetails":null,
               "environmentVariables":null,
               "location":"internal"
            },
            "version":"version",
            "description":"capability2 description",
            "isOpenSource":true,
            "name":"capability2 test",
            "apiBaseUrl":null,
            "dataDeletionEndpointDetails":{
               "apiKey":"apiKey",   # pragma: allowlist secret
               "description":"description",
               "deletionEndpoint":"deletionEndpoint"
            }
         }
      ],
      "minUserPrivacyLevel":5,
      "requiredBuildingBlocks":[
         "App Config",
         "Talent Chooser"
      ],
      "minEndUserRoles":[
         "alumni",
         "employee"
      ],
      "startDate":"2020/06/15T12:06:55",
      "endDate":"2020/10/25T12:06:55",
      "dataDescription":"Data description",
      "selfCertification":{
         "dataDeletionUponRequest":"data deletion upon request",
         "discloseAds":"disclose ads"
      }
   }
```

### POST reviewer for creating contribution reviewer:
The app will post with given information to the endpoint
```
curl -X POST -d `{
                   "name":"John Doe",
                   "githubUsername":"jdoe",
                }' -H "Content-Type: application/json" http://localhost:5000/contributions/admin/reviewers
```
API will return newly created ID
```
    {
    "id": "60c0f0ec830d3024040fad31",
    "message": "new reviewer has been added: test"
    }
```
### GET the list of existing reviewers:
To get the list of the existing reviewers
```
curl http://localhost:5000/contributions/admin/reviewers
```
API will return the message
```
    [
        {
            "dateCreated": "2021/06/09T11:48:44",
            "githubUsername": "jdoe",
            "name": "John Doe"
        }
    ]
```
### DELETE existing contribution dataset
Deletion of the existing reviewer
```
curl -X DELETE http://localhost:5000/contributions/admin/reviewers/60c0f0ec830d3024040fad31
```
API will return the message
```
    {
       "ID":"60c0f0ec830d3024040fad31"
    }
```