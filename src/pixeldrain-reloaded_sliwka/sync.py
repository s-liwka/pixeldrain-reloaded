import requests
import os
import base64

url = "https://pixeldrain.com/api/file/"

# Returns information about a file
def get_info(file_id):
    """
    Get information about a file on Pixeldrain.

    Parameters:
        file_id (str): The ID of the file.

    Returns:
        dict: A dictionary containing file information.
    """
    if "https://" in file_id:
        file_id = file_id.strip("https://pixeldrain.com/u/")
    
    return requests.get(f"https://pixeldrain.com/api/file/{file_id}/info").json()


# Upload a file to Pixeldrain
def upload_file(file_path, returns: str = None, filename: str = None, api_key=None):
    """
    Uploads a file to Pixeldrain synchronously.

    Parameters:
        file_path (str): The path to the file to be uploaded.
        returns (str, optional): Specifies what to return.
            - None or 'dict': Returns a json response.
            - 'verbose_dict': Returns get_info() from the uploaded file.
            - 'id': Returns only the ID of the uploaded file.
            - 'url': Returns a ready-to-use URL to the uploaded file.
        filename (str, optional): Name of the file to upload.
        api_key (str, optional): Pixeldrain API key for authorized uploads.

    Returns:
        dict or str: Depending on the 'returns' parameter, returns a dictionary or a string.
    """
    if api_key is not None:
        headers = {
            "Authorization": "Basic " + base64.b64encode(f":{api_key}".encode()).decode(),
        }
    else:
        headers = {}

    data = {
        "name": os.path.basename(file_path) if filename is None else filename,
        "anonymous": False if api_key is not None else True,
    }

    try:
        response = requests.post(
            url,
            data=data,
            headers=headers,
            files={"file": open(file_path, "rb")}
        )

        response.raise_for_status()
        if returns == 'dict' or returns is None:
            return response.json()
        elif returns == 'verbose_dict':
            return get_info(response.json()['id'])
        elif returns == 'id':
            return response.json()['id']
        elif returns == 'url':
            return f"https://pixeldrain.com/u/{response.json()['id']}"
        else:
            return "Invalid 'returns' parameter. Choose from <dict, verbose_dict, id, url> or None"

    except Exception as e:
        return e


# Download a file from Pixeldrain
def download_file(file_id, path, filename: str = None):
    """
    Download a file from Pixeldrain synchronously.

    Parameters:
        file_id (str): The ID of the file or a Pixeldrain URL.
        path (str): The local path to save the downloaded file.
        filename (str, optional): Name to save the file as (default is Pixeldrain filename).

    Returns:
        str: The path to the downloaded file.
    """
    if "https://" in file_id:
        file_id = file_id.strip("https://pixeldrain.com/u/")

    try:
        if filename is None:
            filename = get_info(file_id)['name']

        with open(os.path.join(path, filename), "wb") as f:
            f.write(requests.get(url + file_id).content)

        return os.path.join(path, filename)

    except Exception as e:
        return e