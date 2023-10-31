# Pixeldrain Reloaded

This is a Python library for interacting with Pixeldrain, a simple file sharing service. It provides synchronous and asynchronous functions for uploading, downloading, and retrieving information about files on Pixeldrain; anonymously and with an API key.

## Installation

soon

## Usage

### Synchronous Version

#### Get Information about a File

```python
file_info = pixeldrain.get_info(file_id="your_file_id")
print(file_info)
```

#### Upload a File

```python
file_path = "path/to/your/file.txt"
response = pixeldrain.upload_file(file_path, returns="dict", filename="custom_filename", api_key="your_api_key")
print(response)
```

#### Download a File

```python
file_id = "your_file_id"
download_path = "path/to/download"
downloaded_file = pixeldrain.download_file(file_id, download_path, filename="custom_filename")
print(f"File downloaded to: {downloaded_file}")
```

### Asynchronous Version

#### Get Information about a File (Async)

```python
file_info = await async_pixeldrain.get_info(file_id="your_file_id")
print(file_info)
```

#### Upload a File (Async)

```python
file_path = "path/to/your/file.txt"
response = await async_pixeldrain.upload_file(file_path, returns="dict", filename="custom_filename", api_key="your_api_key")
print(response)
```

#### Download a File (Async)

```python
file_id = "your_file_id"
download_path = "path/to/download"
downloaded_file = await async_pixeldrain.download_file(file_id, download_path, filename="custom_filename")
print(f"File downloaded to: {downloaded_file}")
```

## Documentation

### `get_info(file_id)`

Get information about a file on Pixeldrain.

- Parameters:
  - `file_id` (str): The ID of the file.

- Returns:
  - `dict`: A dictionary containing file information.

### `upload_file(file_path, returns=None, filename=None, api_key=None)`

Upload a file to Pixeldrain synchronously.

- Parameters:
  - `file_path` (str): The path to the file to be uploaded.
  - `returns` (str, optional): Specifies what to return.
  - `filename` (str, optional): Name of the file to upload.
  - `api_key` (str, optional): Pixeldrain API key for authorized uploads.

- Returns:
  - `dict` or `str`: Depending on the 'returns' parameter, returns a dictionary or a string.

### `download_file(file_id, path, filename=None)`

Download a file from Pixeldrain synchronously.

- Parameters:
  - `file_id` (str): The ID of the file or a Pixeldrain URL.
  - `path` (str): The local path to save the downloaded file.
  - `filename` (str, optional): Name to save the file as (default is Pixeldrain filename).

- Returns:
  - `str`: The path to the downloaded file.

### Asynchronous functions

The asynchronous version of the library provides the same functionality but is designed for use with `asyncio` and `aiohttp` for non-blocking asynchronous operations.

## Special Thanks

[FayasNoushad for the original library](https://github.com/FayasNoushad/Pixeldrain)

## License

This library is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
