import os
import tempfile
import boto3
from .localfile import deletefile
from flask import current_app
import controllers.configs as cfg


class S3EventsImages:
    def __init__(self):
        self.bucket = cfg.BUCKET
        self.client = boto3.client('s3')

    def download(self, event_id, image_id):
        try:
            fileobj = '%s/%s/%s.jpg' % (cfg.AWS_IMAGE_FOLDER_PREFIX, event_id, image_id)
            _, tmpfolder = os.path.split(tempfile.mkdtemp())
            tmpfolder = cfg.IMAGE_FILE_MOUNTPOINT + tmpfolder
            os.mkdir(tmpfolder)
            tmpfile = os.path.join(tmpfolder, event_id+"."+image_id)
            with open(tmpfile, 'wb') as f:
                self.client.download_fileobj(self.bucket, fileobj, f)
        except Exception as ex:
            deletefile(tmpfile)
            raise
        return tmpfile

    def delete(self, event_id, image_id):
        try:
            fileobj = '%s/%s/%s.jpg' % (cfg.AWS_IMAGE_FOLDER_PREFIX, event_id, image_id)
            if not self.__find(event_id, image_id):
                raise
            self.client.delete_object(Bucket=self.bucket, Key=fileobj)
        except Exception as ex:
            raise

    def upload(self, imagefile, event_id, image_id):
        try:
            fileobj = '%s/%s/%s.jpg' % (cfg.AWS_IMAGE_FOLDER_PREFIX, event_id, image_id)
            with open(imagefile, 'rb') as f:
                self.client.upload_fileobj(f, self.bucket, fileobj)
        except Exception as ex:
            raise

    def __find(self, event_id, image_id):
        try:
            fileobj = '%s/%s/%s.jpg' % (cfg.AWS_IMAGE_FOLDER_PREFIX, event_id, image_id)
            get_folder_objects = self.client.list_objects_v2(
                Bucket=self.bucket,
                Delimiter='',
                EncodingType='url',
                MaxKeys=1000,
                Prefix=fileobj,
                FetchOwner=False,
                StartAfter=''
            )
            if not get_folder_objects.get('Contents'):
                return False
        except Exception as ex:
            raise
        return True
