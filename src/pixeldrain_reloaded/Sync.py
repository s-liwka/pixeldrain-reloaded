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

    if not isinstance(file_id, str):
            raise TypeError("file_id must be a string")

    try:

        if "https://" in file_id:
            file_id = file_id.replace("https://pixeldrain.com/u/", '')
        
        return requests.get(f"https://pixeldrain.com/api/file/{file_id}/info").json()

    except Exception as e:
        raise Exception(f"Error while getting file info: {e}")


def upload_file(path, returns: str = None, filename: str = None, api_key: str = None):
    """
    Uploads a file to Pixeldrain synchronously.

    Parameters:
        path (str): The path to the file to be uploaded.
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

    if not isinstance(path, str):
        raise TypeError("path must be a string")

    if returns is not None and returns not in ['dict', 'id', 'url', 'verbose_dict']:
        raise TypeError("returns must be a string: dict, id, url, or verbose_dict")

    if filename is not None and not isinstance(filename, str):
        raise TypeError("filename must be a string")

    if api_key is not None and not isinstance(api_key, str):
        raise TypeError("api_key must be a string")

    try:

        url = "https://pixeldrain.com/api/file"

        if api_key is not None:
            headers = {
                "Authorization": "Basic " + base64.b64encode(f":{api_key}".encode()).decode(),
            }
        else:
            headers = {}

        data = {
            "name": os.path.basename(path) if filename is None else filename,
            "anonymous": False if api_key is not None else True,
        }

        with open(path, "rb") as file:
            files = {"file": (data["name"], file)}

            response = requests.post(url, data=data, headers=headers, files=files)

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
                raise Exception('wtf')

    except Exception as e:
        raise Exception(f"Error while uploading file: {e}")


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

    if not isinstance(file_id, str):
        raise TypeError("file_id must be a string")

    if not isinstance(path, str):
        raise TypeError("path must be a string")

    if filename is not None and not isinstance(filename, str):
        raise TypeError("filename must be a string")

    try:

        if "https://" in file_id:
            file_id = file_id = file_id.replace("https://pixeldrain.com/u/", '')

        if filename is None:
            filename = get_info(file_id)['name']

        with open(os.path.join(path, filename), "wb") as f:
            f.write(requests.get(f"https://pixeldrain.com/api/file/{file_id}").content)

        return os.path.join(path, filename)

    except Exception as e:
        raise Exception(f"Error while downloading file: {e}")


def get_thumbnail(file_id, returns_url: bool = False, width: int = None, height: int = None):
    """
    Returns a PNG thumbnail image representing the file. The thumbnail image will be 128x128 px by default.
    The width and height parameters need to be a multiple of 16. Allowed values are 16, 32, 48, 64, 80, 96, 112, and 128. 
    If a thumbnail cannot be generated for the file, you will be redirected to a mime type image of 128x128 px.

    Parameters:
        file_id (str): ID of the file to get a thumbnail for. If the file_id is a URL, it will be extracted.
        returns_url (bool, optional): By default, the function returns bytes, but you may specify it to return an URL to the thumbnail by setting this parameter to True.
        width (int, optional): Width of the thumbnail image.
        height (int, optional): Height of the thumbnail image.

    Returns:
        The function will return either bytes or URL depending on the returns parameter (default is bytes):
            bytes/str: If a thumbnail can be generated, the PNG image bytes are returned.
            bytes/str: If a thumbnail cannot be generated, a 301 redirect occurs to the URL of an image representing the type of the file.
    """

    if not isinstance(file_id, str):
        raise TypeError("file_id must be a string")

    if not isinstance(returns_url, bool):
        raise TypeError("returns_url must be a boolean")

    if width is not None and not isinstance(width, int):
        raise TypeError("width must be an integer")

    if height is not None and not isinstance(height, int):
        raise TypeError("height must be an integer")

    try:

        if "https://" in file_id:
            file_id = file_id.strip("https://pixeldrain.com/u/")

        t = f"https://pixeldrain.com/api/file/{file_id}/thumbnail"

        params = {}
        if width is not None:
            params['width'] = width
        if height is not None:
            params['height'] = height

        response = requests.get(t, params=params)

        if response.status_code == 200:
            if returns_url:
                return response.url
            else:
                return response.content
        elif response.status_code == 301:
            if returns_url:
                return response.url
            else:
                return response.content
        else:
            raise Exception(f"Status code {response.status}")

    except Exception as e:
        raise Exception(f"Error while fetching the thumbnail: {e}")


def delete_file(file_id, api_key):
    """
    Delete a file from Pixeldrain using the provided file ID and API key.

    Parameters:
        file_id (str): The unique identifier of the file to be deleted. If the full URL is provided, it will be extracted to obtain the file ID.
        api_key (str): The API key required for authorization to delete the file.

    Returns:
        dict: A dictionary containing information about the deleted file, as returned by the Pixeldrain API.
    """

    if not isinstance(file_id, str) or not isinstance(api_key, str):
        raise TypeError("file_id and api_key must be strings")

    try:
        if "https://" in file_id:
            file_id = file_id.replace("https://pixeldrain.com/u/", '')
        
        headers = {
            "Authorization": "Basic " + base64.b64encode(f":{api_key}".encode()).decode(),
        }

        response = requests.delete(
            headers=headers,
            url=f"https://pixeldrain.com/api/file/{file_id}"
        )

        response.raise_for_status()
        return response.json()

    except Exception as e:
        raise Exception(f"Error while deleting the file: {e}")