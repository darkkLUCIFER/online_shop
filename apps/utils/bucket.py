import os

import boto3
from django.conf import settings


class Bucket:
    """CDN Bucket manager

    This class provides methods to interact with an S3-compatible storage service.
    It allows listing, uploading, downloading, and deleting objects in the bucket.

    NOTE:
        None of these methods are async. To use them asynchronously, invoke them
        from an async-capable context such as Celery tasks in `tasks.py`.
    """
    __instance = None

    def __init__(self):
        # Create a new session with boto3 using provided AWS settings
        session = boto3.session.Session()
        self.connection = session.client(
            service_name=settings.AWS_SERVICE_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        )

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = Bucket()

        return cls.__instance

    def get_objects(self):
        """
            List all objects in the specified S3 bucket.

            This method uses `list_objects_v2` to retrieve a dictionary containing
            metadata about the objects in the bucket, such as keys and file sizes.

            Returns:
                dict: A dictionary containing information about the objects in the bucket.
        """
        result = self.connection.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        return result

    def delete_object(self, key):
        """
            Delete a specific object from the S3 bucket.

            Args:
                key (str): The key (path) of the object to delete in the bucket.

            Returns:
                bool: True if the object was deleted successfully.
        """
        self.connection.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        return True

    def download_object(self, key):
        """
            Download a specific object from the S3 bucket to the local file system.

            Args:
                key (str): The key (path) of the object in the bucket to download.

            Returns:
                None
        """
        # Extract the file name from the key (path in the bucket)
        file_name = key.split('/')[-1]
        aws_local_storage_dir = settings.AWS_LOCAL_STORAGE

        # Check if the local storage directory exists, and create it if it doesn't
        if not os.path.exists(aws_local_storage_dir):
            os.makedirs(aws_local_storage_dir)

        # Download the object from the S3 bucket to the local storage directory
        with open(settings.AWS_LOCAL_STORAGE + file_name, "wb") as f:
            self.connection.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, key, f)

    def upload_object(self, file_path, key=None):
        """
        Upload a file to the S3 bucket.

        Args:
            file_path (str): The path to the local file to upload.
            key (str): The desired key (path) in the S3 bucket. If not provided, the
                       base name of the file_path will be used.

        Returns:
            None
        """
        # If no key is provided, use the base name of the file path
        if key is None:
            key = os.path.basename(file_path)

        # Open the file and upload it to the S3 bucket
        with open(file_path, "rb") as f:
            self.connection.upload_fileobj(f, settings.AWS_STORAGE_BUCKET_NAME, key)
