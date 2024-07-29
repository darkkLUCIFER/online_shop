from apps.utils.bucket import Bucket


# TODO: can be async!?
def get_all_bucket_objects_task():
    result = Bucket.get_instance().get_objects()
    if result['KeyCount']:
        return result['Contents']
    else:
        return None
