from typing import Union

import aiohttp

DEFAULT_HEADERS = {
    "User-Agent": "Ayo Discord Bot (Discord: yarkis01)",
    "From": "yarkis@ik.me"
}

async def make_api_request(url, headers: dict = None, timeout: float = 10.0) -> Union[dict, None]:
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