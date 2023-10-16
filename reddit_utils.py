import requests
from requests.auth import HTTPBasicAuth

from creds import CLIENT_ID, CLIENT_SECRET, USER_NAME, PASSWORD


def get_reddit_auth():
    """
    Will get an oauth access token from reddit.
    :return: The access token to use for reddit's api
    """
    data = {
        "grant_type": "password",
        "username": USER_NAME,
        "password": PASSWORD
    }
    resp = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=HTTPBasicAuth(username=CLIENT_ID, password=CLIENT_SECRET),
        headers={"User-Agent": "MyAPI/0.0.1"},
        data=data
    )
    return resp.json()["access_token"]

def search_subreddits(token, query=None):
    """
    Will search for all subreddits that match a given query
    :param token: The oauth access token for reddit.
    :param query: The query term to search for
    :return: A list of all subreddits that match the query
    """

    # If there is no query, just get the most popular subreddits by removing /search from the url
    url = "https://oauth.reddit.com/subreddits" + ("/search" if query is not None else "")
    next_page = None
    subreddits = []

    # The maximum number of pages is 50
    for i in range(50):

        # Make the api request
        print(f"Requesting Subreddits {i * 100} to {(i + 1) * 100} for {query}")
        params = {"limit": 1000, "after": next_page, 'q': query}
        headers = { "User-Agent": "PostmanRuntime/7.33.0", "Authorization": f"bearer {token}"}
        resp = requests.get(url=url, params=params, headers=headers)
        resp.raise_for_status()

        # Extract the pertinent info
        resp = resp.json().get("data", {})
        subreddits += resp.get("children", [])
        if not (next_page := resp.get("after")):
            break
    return subreddits