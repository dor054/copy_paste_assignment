import logging
import time
import os

import azure.functions as func
from azure.storage.blob import BlobServiceClient


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    filename = req_body.get('filename')
    url = req_body.get('url')

    CONNECTION_STRING = os.environ["CUSTOMCONNSTR_df_storage_conn_str1"]
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    copied_blob = blob_service_client.get_blob_client("df-first-container", filename)
    copied_blob.start_copy_from_url(url)

    for i in range(6):
        props = copied_blob.get_blob_properties()
        status = props.copy.status
        logging.debug(f"Copy status: {status}")
        if status == "success":
            # Copy finished
            break
        time.sleep(10)

    if status != "success":
        # if not finished after 1min, cancel the operation
        logging.error("Copying file didn't complete within 1 min")
        props = copied_blob.get_blob_properties()
        logging.debug(props.copy.status)
        copy_id = props.copy.id
        copied_blob.abort_copy(copy_id)
        props = copied_blob.get_blob_properties()
        logging.debug(props.copy.status)

    if status == "success":
        return func.HttpResponse(f"Filename, {filename} has been copied successfully to stotage account.", status_code=200)
    else:
        return func.HttpResponse(f"There was a problem to copy file {filename} to storage account.", status_code=500)

