import aiohttp
import asyncio
import os
import base64
import json
import aiofiles

url = "https://pixeldrain.com/api/file/"


# Returns information about a file
async def async_get_info(file_id):
    """
    Get information about a file on Pixeldrain.

    Parameters:
        file_id (str): The ID of the file or the url (it will get stripped if its an url).

    Returns:
        dict: A dictionary containing file information.
    """

    if not isinstance(file_id, str):
            raise TypeError("file_id must be a string")

    try:
        if "https://" in file_id:
            file_id = file_id.replace("https://pixeldrain.com/u/", '')

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://pixeldrain.com/api/file/{file_id}/info") as response:
                return await response.json()

    except Exception as e:
        raise Exception(f"Error while getting file info: {e}")


async def async_upload_file(path, returns: str=None, filename: str=None, api_key: str=None):
    """
    Uploads a file to Pixeldrain asynchronously.

    Parameters:
        path (str): The path to the file to be uploaded.
        returns (str, optional): Specifies what to return.
            - None or 'dict': Returns a json response.
            - 'verbose_dict': Returns async_get_info() from the uploaded file.
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
    
    if api_key is not None:
        headers = {
            "Authorization": "Basic " + base64.b64encode(f":{api_key}".encode()).decode(),
        }
    else:
        headers = {}

    async with aiohttp.ClientSession() as session:
        async with aiofiles.open(path, "rb") as f:
            data = {
                "file": await f.read(),
                "name": os.path.basename(path) if filename is None else filename,
                "anonymous": 'True' if api_key is not None else 'False' # bools are strings because pixeldrain is silly
            }
            async with session.post(url, data=data, headers=headers) as response:
                if response.status == 201:
                    if returns == 'dict' or returns is None:
                        return json.loads(await response.text())
                    if returns == 'verbose_dict':
                        return await async_get_info(json.loads(await response.text())['id'])
                    elif returns == 'id':
                        return json.loads(await response.text())['id']
                    elif returns ==  'url':
                        return f"https://pixeldrain.com/u/{json.loads(await response.text())['id']}"
                    else:
                        return "Invalid returns parameter. returns=<dict, verbose_dict, id, url> or None"
                else:
                    raise Exception(f"Error uploading file. Status code: {response.status}")

# Download a file from Pixeldrain
async def async_download_file(file_id, path, filename: str = None):
    """
    Download a file from Pixeldrain asynchronously.

    Parameters:
        file_id (str): The ID of the file or a Pixeldrain URL (if an URL is provided, it will get stripped to an ID).
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

    if "https://" in file_id:
        file_id = file_id.strip("https://pixeldrain.com/u/")

    try:
        if filename is None:
            file_info = await async_get_info(file_id)
            filename = file_info['name']


        async with aiohttp.ClientSession() as session:
            async with session.get(url + file_id) as response:
                content = await response.read()

        async with aiofiles.open(os.path.join(path, filename), "wb") as f:
            await f.write(content)

        return os.path.join(path, filename)

    except Exception as e:
        raise Exception(f"Error while downloading file: {e}")


async def async_get_thumbnail(file_id, returns_url: bool=False, width: int=None, height: int=None):
    """
    Returns a PNG thumbnail image representing the file. The thumbnail image will be 128x128 px by default.
    The width and height parameters need to be a multiple of 16. Allowed values are 16, 32, 48, 64, 80, 96, 112, and 128. 
    If a thumbnail cannot be generated for the file, you will be redirected to a mime type image of 128x128 px.

    Parameters:
        file_id (str): ID of the file to get a thumbnail for. If the file_id is a URL, it will be extracted.
        returns_url (bool, optional): By default the function returns bytes, but you may specify it to return an URL to the thumbnail by setting this parameter to True.
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
            file_id = file_id.replace("https://pixeldrain.com/u/", '')

        t = f"https://pixeldrain.com/api/file/{file_id}/thumbnail"

        params = {}
        if width is not None:
            params['width'] = width
        if height is not None:
            params['height'] = height

        async with aiohttp.ClientSession() as session:
            async with session.get(t, params=params) as response:
                if response.status == 200:
                    if returns_url:
                        return response.url
                    else:
                        return await response.read()
                elif response.status == 301:
                    if returns_url:
                        return response.url
                    else:
                        return await response.read()
                else:
                    raise Exception(f"Error. Status code {response.status}")

    except Exception as e:
        raise Exception(f"Error while fetching the thumbnail: {e}")



async def async_delete_file(file_id, api_key):
    """
    Delete a file from Pixeldrain using the provided file ID and API key.

    Parameters:
        file_id (str): The unique identifier of the file to be deleted. You may also provide the full URL.
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

        async with aiohttp.ClientSession() as session:
            async with session.delete(url=f"https://pixeldrain.com/api/file/{file_id}", headers=headers) as response:
                response.raise_for_status()
                return await response.json()

    except Exception as e:
        raise Exception(f"Error while deleting the file: {e}")