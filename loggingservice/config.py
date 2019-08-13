import os
# this has to be have the file path to the folder for saving image files and other necessary files from rest service
LOGGING_MONGO_URL = os.getenv('LOGGING_MONGO_URL', 'localhost:27017')
LOGGING_DB_NAME="loggingdb"
LOGGING_COLL_NAME="LogginDataset"