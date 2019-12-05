import os
import ast
from dotenv import load_dotenv

# Load .env file
load_dotenv()

API_LOC = os.getenv('API_LOC', '../../')
DEBUG = os.getenv('DEBUG', 'False')

EVENT_MONGO_URL = os.getenv("EVENT_MONGO_URL", "mongodb://localhost:27017")
EVENT_DB_NAME = os.getenv("EVENT_DB_NAME", "rokwire")
URL_PREFIX = os.getenv("URL_PREFIX", "/events")

IMAGE_COLLECTION = os.getenv("IMAGE_COLLECTION", "images")
IMAGE_FILE_MOUNTPOINT = os.getenv("IMAGE_FILE_MOUNTPOINT", "eventservice/events-images/")
IMAGE_URL = os.getenv("IMAGE_URL", "https://{bucket}.s3-{region}.amazonaws.com/{prefix}/{event_id}/{image_id}.jpg")
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "4194304"))  # 4 * 1024 * 1024
ALLOWED_EXTENSIONS = ast.literal_eval(os.getenv("ALLOWED_EXTENSIONS", "{'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}"))

AWS_IMAGE_FOLDER_PREFIX = os.getenv("AWS_IMAGE_FOLDER_PREFIX", "events")
BUCKET = os.getenv("AWS_S3_BUCKET", "rokwire-events-s3-images")
