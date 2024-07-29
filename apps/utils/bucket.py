import os

import boto3
from django.conf import settings


class Bucket:
    """CDN Bucket manager

    init method created connection

    NOTE:
        none of these methods are async. use public interface in tasks.py modules instead.
    """

    def __init__(self):
        session = boto3.session.Session()
        self.connection = session.client(
            service_name=settings.AWS_SERVICE_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        )

    @staticmethod
    def get_instance():
        return Bucket()

    def get_objects(self):
        result = self.connection.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        return result

    def delete_object(self, key):
        self.connection.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        return True

    def download_object(self, key):
        file_name = key.split('/')[-1]
        aws_local_storage_dir = settings.AWS_LOCAL_STORAGE

        # Check if the directory exists, create it if it doesn't
        if not os.path.exists(aws_local_storage_dir):
            os.makedirs(aws_local_storage_dir)

        with open(settings.AWS_LOCAL_STORAGE + file_name, "wb") as f:
            self.connection.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, key, f)

    def upload_object(self, file_path, key=None):
        """
        Upload a file to the S3 bucket.

        Args:
            file_path (str): The path to the local file to upload.
            key (str): The desired key in the S3 bucket.

        Returns:
            None
        """
        if key is None:
            key = os.path.basename(file_path)

        with open(file_path, "rb") as f:
            self.connection.upload_fileobj(f, settings.AWS_STORAGE_BUCKET_NAME, key)
