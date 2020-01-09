# Events Building Block

The goal of the Events Building Block is to provide a set of RESTFul web services to manage events in the Rokwire platform. This includes adding a new event, retrieving relevant events based on search query, etc.
                      

## Setup Environment
```
cd eventservice
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Environment File

You need to have a .env file in this directory that contains credentials required for authentication.

Example file format:

```
SHIBBOLETH_HOST=<Shibboleth Host Name>
SHIBBOLETH_CLIENT_ID=<Shibboleth Client ID>

ROKWIRE_API_KEY=<Rokwire API Key>
ROKWIRE_ISSUER=<Rokwire ID Token Issuer Name>

# AWS environment variables to set when running on development machine. 
# This is not required when running within AWS.
AWS_ACCESS_KEY_ID=<AWS Access Key ID>
AWS_SECRET_ACCESS_KEY=<AWS Secret Access Key>
```

You also need to set CACHE_DIRECTORY to a valid file folder.
For example:
```
CACHE_DIRECTORY=yourlocalfilefolder
```

## Run in Development Mode

```
cd rokwire-building-blocks-api/eventservice
python api/events_rest_service.py
```
and the Events Building Block should be running at localhost at port 5000 (http://localhost:5000/events).
The detailed API information is in rokwire.yaml in the OpenAPI Spec 3.0 format.

## Run as Docker Container in Local
```
cd rokwire-building-blocks-api
docker build -f eventservice/Dockerfile -t rokwire/events-building-block .
docker run --rm --name events --env-file eventservice/.env -p 5000:5000 rokwire/events-building-block
```
You need to edit config.py where you have to specify mongo url.
```
EVENT_MONGO_URL="mongodb://MongoDBMachinePublicIP:27017"
EVENT_DB_NAME="eventdb"
```

## AWS ECR Instructions

Make sure the repository called rokwire/eventservice exists in ECR. Then create Docker image for Rokwire Platform API and push to AWS ECR for deployment.

```
cd rokwire-building-blocks-api 
docker build -f eventservice/Dockerfile -t rokwire/events-building-block .
docker tag rokwire/events-building-block:latest 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/eventservice:latest
$(aws ecr get-login --no-include-email --region us-east-2)
docker push 779619664536.dkr.ecr.us-east-2.amazonaws.com/rokwire/eventservice:latest
```

## Sample Events for Post Endpoint:

Let us use ```curl``` command to post two sample events to the Events Building Block running at `http://localhost:5000/events`.


```
curl -d '{
        "tags": ["social", "reading", "coffee"],
        "title": "Reading Day at KCPA",
        "category": "Community",
        "targetAudience": ["students", "alumni", "faculty", "public"],
        "sponsor": "Krannert Center for the Performing Arts",
        "startDate": "2019/05/02T11:00:00",
        "endDate": "2019/05/02T16:00:00",
        "description": "Looking for a casual place to study on Reading Day from 11am-4pm? Krannert Center has got your back: plenty of seating with charging stations, delicious food and beverages available for purchase from Intermezzo cafe, and more.",
        "location": {
            "latitude": 40.1078955,
            "longitude": -88.224036,
            "floor": 2,
            "description": "Krannert Center, 2nd floor"
        }
    }' -H "Content-Type: application/json" -X POST http://localhost:5000/events
```

```
curl -d '{
        "tags": ["pi", "pie", "ncsa", "coffee"],
        "title": "Celebrate Mathematic Pi Day",
        "category": "Community",
        "targetAudience": ["staff"],
        "sponsor": "NCSA",
        "startDate": "2019/04/25T13:00:00",
        "endDate": "2019/04/25T16:00:00",
        "description": "celerate mathematic Pi-day at NCSA",
        "location": {
            "latitude": 40.1147743,
            "longitude": -88.2252053,
            "floor": 1,
            "description": "NCSA, 1st floor"
        }
    }' -H "Content-Type: application/json" -X POST http://localhost:5000/events
```

It will return back the `post` status in json which includes the internal id as below:

```
{
  	"status": 201,
	"id": "5cd1f7294207d970db70ea92",
	"message": "[POST]: event record created: id = 5cd1f7294207d970db70ea92"
}
```

## One Example of Using Put Endpoint:

Put endpoint allows to replace an existing event with a new one. For example, we can use ```curl``` command to replace one existing event: 
```
curl -d '{
        "tags": ["pi", "pie", "ncsa", "coffee"],
        "title": "We Celebrate Mathematic Pi Day",
        "category": "Community",
        "targetAudience": ["staff", "guest"],
        "sponsor": "NCSA",
        "startDate": "2019/04/25T13:00:00",
        "endDate": "2019/04/25T16:00:00",
        "description": "celerate mathematic Pi-day at NCSA",
        "location": {
            "latitude": 40.1147743,
            "longitude": -88.2252053,
            "floor": 1,
            "description": "NCSA, 1st floor"
        }
    }' -H "Content-Type: application/json" -X PUT http://localhost:5000/events/5cd1f7294207d970db70ea92
```
It will return back the `put` status in json, where the `nUpdate` denotes how many event records have been updated:
```
{
	"status": 200,
	"id": "5cd1f7294207d970db70ea92",
	"message": "[PUT]: event id 5cd1f7294207d970db70ea92, nUpdate = 1 "
}
```

## One Example of Using Patch Endpoint:

Patch endpoint allows to update an existing event record. For example, we can use `Curl` command to update the `title` field of the current event: 
```
curl -d '{"title": "NCSA Celebrates Mathematics Pi Day"}' -X PATCH http://localhost:5000/events/5cd1f7294207d970db70ea92
```
You can also update geolocation coordinates. For example, we can update the latitude of location to this new value:
```
curl -d '{"location.latitude": 40.10789}' -X PATCH http://localhost:5000/events/5cd1f7294207d970db70ea92
```
It will return back the `patch` status in json, where the `nUpdate` denotes how many event records have been updated:
```
{
	"status": 200,
	"id": "5cd1f7294207d970db70ea92",
	"message": "[UPDATE]: event id 5cd1ecb94207d96e66ca2e67, nUpdate = 1 "
}
```

## One Example of Using Delete Endpoint:

Delete endpoint allows to delete an event record from the backend storage.
```
curl -X DELETE http://localhost:5000/events/5cd1f7294207d970db70ea92
```
It will return back the `deletion` status in json, where the `nDelete` denotes how many event records have been deleted:
```
{
	"status": 202,
	"id": "5cd1f7294207d970db70ea92",
	"message": "[DELETE]: event id 5cd1ecb94207d96e66ca2e67, nDelete = 1 "
}
```

## One Example of Getting Categories Endpoint:
```
curl -X GET http://localhost:5000/events/categories
```

It will return back a list of main categories and sub categories:
```
[
  {
    "category": "Entertainment"
  }, 
  {
    "category": "Academic"
  }, 
  {
    "category": "Community"
  }, 
  {
    "category": "Career Development"
  }, 
  {
    "category": "Recreation"
  }, 
  {
    "category": "Athletics", 
    "subcategories": [
      "Baseball", 
      "Men's Basketball", 
      "Men's Cross Country", 
      "Football", 
      "Men's Golf", 
      "Men's Gymnastics", 
      "Men's Tennis", 
      "Men's Track & Field", 
      "Wrestling", 
      "Women's Basketball", 
      "Women's Cross Country", 
      "Women's Golf", 
      "Women's Gymnastics", 
      "Women's Soccer", 
      "Softball", 
      "Swim & Dive", 
      "Women's Tennis", 
      "Women's Track & Field", 
      "Volleyball"
    ]
  }, 
  {
    "category": "Other"
  }
]
```


## Query Search Examples:

### Tilte Search:

This query will return back all events whose title contains the word `pi`.
```
/events?title=pi
```
This query will return back all events whose title contains the word `pi` and `day`.
```
/events?title=pi&title=day
```

### Tags Search:

This query will return all events whose tags contain ``coffee`` `or` ``music``.

```
/events?tags=coffee&tags=music
```

### Target Audience Search:

**Note: This feature in search has been temporarily turned off.**
This query will return all events whose target audience is either ``student`` or ``staff``.

```
/events?targetAudience=students&targetAudience=staff
```

### DateTime Range Search:

This query will return back all events whose startdate and enddate between the range.
```
/events?startDate=2019-04-25T13:00:00&endDate=2019-04-25T17:00:00
```

### Geolocation Radius Search

This query will return back all events whose geolocation is within ``800`` meter centered at given geolocation point.
```
/events?latitude=40.1078955&longitude=-88.224036&radius=800
```

### Category Search
This query supports main categories search and main/sub categories search. The request can use  `.` to concatenate the search on the combination of the main category and sub category. It can also use `&` to append more category search. In the below search example, the result will contains all the events whose main category is `Athletics` and meanwhile the sub category must be `Football`. The result also contains all the events whose main category is `Community`.
```
/events?category=Athletics.Football&category=Community
```

## MongoDB

You can import predefined categories into the local mongodb.
mongoimport --db eventdb --collection categories --file categories.json

Events platform uses MongoDB to facilitate the indexing and searching. Before executing the query search, MongoDB need to enable
text index and geospatial index.

Please refer to: 

https://docs.mongodb.com/manual/text-search/

https://docs.mongodb.com/manual/geospatial-queries/

```
db.events.createIndex({'title': "text"})
db.events.createIndex({'startDate': -1})
db.events.createIndex({'endDate': -1})
db.events.createIndex({'sponsor': 1})
db.events.createIndex({'categorymainsub': 1})
db.events.createIndex({'coordinates': "2dsphere"})
```

