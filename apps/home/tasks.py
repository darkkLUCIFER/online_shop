from apps.utils.bucket import Bucket
from celery import shared_task


# TODO: can be async!?
def get_all_bucket_objects_task():
    result = Bucket.get_instance().get_objects()
    if result['KeyCount']:
        return result['Contents']
    else:
        return None


@shared_task
def delete_object_task(key):
    Bucket.get_instance().delete_object(key)


@shared_task
def download_object_task(key):
    Bucket.get_instance().download_object(key)


@shared_task
def upload_object_task(file_path):
    Bucket.get_instance().upload_object(file_path)
