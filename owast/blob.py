import azure.storage.blob

ACCOUNT_URL = 'https://blob'


def get_service_client():
    return azure.storage.blob.BlobServiceClient(ACCOUNT_URL)


def get_blob_client(*args, **kwargs):
    service_client = get_service_client()
    return service_client.get_blob_client(*args, **kwargs)
