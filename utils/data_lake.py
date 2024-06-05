from azure.appconfiguration.aio import BlobServiceClient, ResourceExistsError


def write_data_to_blob(connection_string, container_name, data, blob_name):
    """
    Writes data directly to a blob in Azure Blob Storage.
    
    :param connection_string: Azure Blob Storage connection string
    :param container_name: Name of the container where data will be stored
    :param data: Data to be written to the blob, as a string or bytes
    :param blob_name: Name of the blob where data will be written
    :return: None
    """
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
   
    try:
        container_client = blob_service_client.create_container(container_name)
    except ResourceExistsError:
        container_client = blob_service_client.get_container_client(container_name)

    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(data, overwrite=True)