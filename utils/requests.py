from typing import Union
import json

from deepdiff import DeepDiff
import aiohttp

from utils.logger import Logger

DEFAULT_HEADERS = {
    "User-Agent": "Ayo Discord Bot (Discord: yarkis01)",
    "From": "yarkis@ik.me"
}

async def make_api_request(url: str, headers: dict = None, timeout: float = 10.0) -> Union[dict, None]:
    """
    Make an asynchronous API request with default headers.

    Args:
        url (str): The URL of the API endpoint
        headers (dict): Optional additional headers to add
        timeout (float): Optional timeout in seconds, default 10.0

    Returns:
        dict: The JSON response data if the request was successful
        None: If any error occurred
    """
    merged_headers = {**DEFAULT_HEADERS, **headers} if headers else DEFAULT_HEADERS.copy()

    try:
        async with aiohttp.ClientSession(timeout = aiohttp.ClientTimeout(timeout), headers = merged_headers) as session:
            async with session.get(url) as response:
                return await response.json() if response.status == 200 else None
    except Exception:
        return None


async def update_data_if_needed(url: str, path: str) -> None:
    """
    Check if the JSON data in the file at 'path' needs to be updated 
    from the 'url' API endpoint. If so, update the file with new data.

    Args:
        url (str): The API endpoint URL
        path (str): The path to the JSON file
    
    Returns:
        None
    """
    request = await make_api_request(url)
    
    if not request:
        Logger.fail(f"Unable to check whether \"{path}\" file should be updated.", "update")
        return
    
    data = json.load(open(path))
    if DeepDiff(data, request, ignore_string_case = True) != {}:
        Logger.warning(f"The \"{path}\" file must be updated.", "update")
        
        with open(path, "w") as json_file:
            json.dump(request, json_file)
            Logger.success(f"The \"{path}\" file has been successfully updated!", "update")
