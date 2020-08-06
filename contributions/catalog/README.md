# Contribution-Catalog

## Run in Development Mode
MongoDB's service needs to be started and a Mongo Shell needs to be connected in a separate terminal instance

- For MacOS
```
brew services start mongodb-community@4.2
mongo
```

- Ubuntu (The daemon-reload command isn't required)
```
sudo systemctl daemon-reload
sudo systemctl start mongod
mongo
```

This repository should be put inside `/catalog` and run outside the folder. 
There are two ways to do so:

The first one:

- (Linux or MAC):
```
export FLASK_APP=catalog
export FLASK_ENV=development
flask run
```

- (Windows):
```
set FLASK_APP=catalog
set FLASK_ENV=development
flask run
```

The second one:

- create a file called .flaskenv
- fill in file with:
    - FLASK_APP=\_\_init\_\_.py
    - FLASK_ENV=development
    - FLASK_DEBUG=1

## Setup Environment and start the catalog application
- (Linux or MAC):
```
cd catalog
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
cd .. 
set FLASK_APP=catalog
set FLASK_ENV=development
flask run --port=5050
```
- (Windows):
```
cd catalog
py -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
cd .. 
set FLASK_APP=catalog
set FLASK_ENV=development
flask run --port=5050
```

The following environment variables need to be set when running on development machine. 
This is not required when running within AWS.
```
AWS_ACCESS_KEY_ID=<AWS Access Key ID>
AWS_SECRET_ACCESS_KEY=<AWS Secret Access Key>
```


## MongoDB Setup
MongoDB needs to be installed for the flask app to run and interface with a database

- For MacOS, prerequisites are having XCode and Homebrew
```
brew tap mongodb/brew
brew install mongodb-community@4.2
```
- For Ubuntu LTS releases
```
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
```
The above should work, but in case a gnupg error is encountered
```
sudo apt-get install gnupg
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
```
Create a list file for MongoDB
```
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
```
Reload and Install
```
sudo apt-get update
sudo apt-get install -y mongodb-org
```

The template setup configuration exists in config.py.template, to run locally a new file config.py needs to be created accounting for changes based on your local environment setup.  
