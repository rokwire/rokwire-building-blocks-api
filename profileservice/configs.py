import os

profile_mongo_url = os.getenv('MONGODB_URI', 'localhost:27017')
profile_db_name = os.getenv('DB_NAME', 'profiledb')
profile_db_coll_name = os.getenv('DB_COLLECTION', 'ProfileDataset')
profile_rest_storage = 'C:\\rest'
