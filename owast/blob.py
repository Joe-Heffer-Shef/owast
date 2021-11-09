"""
Azure Blob Storage
"""

import azure.storage.blob

# Default Azurite credentials
# https://github.com/Azure/Azurite#connection-strings
BLOB_ENDPOINT = 'http://blob:10000/devstoreaccount1'
CONN_STR = f'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint={BLOB_ENDPOINT};'


def get_service_client():
    return azure.storage.blob.BlobServiceClient.from_connection_string(CONN_STR)


def get_blob_client(*args, **kwargs):
    service_client = get_service_client()
    return service_client.get_blob_client(*args, **kwargs)
