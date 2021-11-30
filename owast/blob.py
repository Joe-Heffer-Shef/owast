"""
Azure Blob Storage
"""

import os

import azure.storage.blob

# Default Azurite credentials
# https://github.com/Azure/Azurite#connection-strings
CONN_STR = os.environ['BLOB_CONN_STR']


def get_service_client(conn_str: str = None, *args,
                       **kwargs) -> azure.storage.blob.BlobServiceClient:
    return azure.storage.blob.BlobServiceClient.from_connection_string(
        conn_str=conn_str or CONN_STR, *args, **kwargs)
