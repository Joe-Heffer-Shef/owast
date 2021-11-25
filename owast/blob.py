"""
Azure Blob Storage
"""

import os

import azure.storage.blob

# Default Azurite credentials
# https://github.com/Azure/Azurite#connection-strings
BLOB_ENDPOINT = os.getenv('BLOB_ENDPOINT',
                          'http://localhost:10000/devstoreaccount1')
CONN_STR = f'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint={BLOB_ENDPOINT};'


def get_service_client(conn_str: str = None, *args,
                       **kwargs) -> azure.storage.blob.BlobServiceClient:
    return azure.storage.blob.BlobServiceClient.from_connection_string(
        conn_str=conn_str or CONN_STR, *args, **kwargs)
