import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

EVENT_MONGO_URL=os.getenv("EVENT_MONGO_URL", "mongodb://localhost:27017")
EVENT_DB_NAME=os.getenv("EVENT_DB_NAME", "rokwire")
URL_PREFIX = os.getenv('URL_PREFIX', '/events')

IMAGE_COLLECTION='images'
IMAGE_FILE_MOUNTPOINT="eventservice/events-images/"
MAX_CONTENT_LENGTH=4*1024*1024
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

AWS_IMAGE_FOLDER_PREFIX=os.getenv("AWS_IMAGE_FOLDER_PREFIX", "events")
BUCKET=os.getenv("AWS_S3_BUCKET", "rokwire-events-s3-images")
