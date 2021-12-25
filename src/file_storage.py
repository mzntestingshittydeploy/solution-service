import logging

import requests

from .models import SignedUrl, File

minizinc_data_name = "minizinc-app"
mzn_data_url = "http://"+minizinc_data_name+"/api/minizinc/upload"  # TODO Take as variable


def drop_file(body: str, user_id: str, computation_id: str):

    # Get upload-url
    headers = {'UserId': 'system', 'Role': 'admin'}
    try:
        response = requests.get(mzn_data_url, headers=headers)
    except requests.exceptions.ConnectionError:
        logging.error("Couldn't connect to {}".format(mzn_data_url))
        return None

    if response.status_code != 200:
        logging.error("minizinc-data replied {}".format(response.text))

    signed_url = SignedUrl.parse_raw(response.text)

    # upload solution
    try:
        response = requests.put(signed_url.url, data=body)
    except requests.exceptions.ConnectionError:
        logging.error("Couldn't connect to {}".format(signed_url.url))
        return None

    if response.status_code != 200:
        logging.error("The S3-Bucket replied {}: {}".format(response.status_code, response.text))

    file_name = computation_id + ".txt"
    data = File(userID=user_id, fileUUID=signed_url.fileUUID, fileName=file_name)
    try:
        response = requests.post("http://"+minizinc_data_name+"/api/minizinc/upload", headers=headers, json=data.dict())
    except requests.exceptions.ConnectionError:
        logging.error("Couldn't connect to {}".format(minizinc_data_name))
        return None

    if response.status_code != 200:
        logging.error("minizinc-data replied {}: {}".format(response.status_code, response.text))

    return (signed_url.fileUUID)
