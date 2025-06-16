import requests

def requests_get(url: str, params: dict = None, headers: dict = None) -> dict:
    """Sends a GET request to the specified URL with optional parameters.

    Args:
        url (str): The URL to send the GET request to.
        params (dict, optional): A dictionary of query parameters to include in the request.

    Returns:
        dict: The JSON response from the server or an error message.
    """
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        return {"status": "success", "data": response.json()}
    except requests.RequestException as e:
        return {"status": "error", "error_message": str(e)}

