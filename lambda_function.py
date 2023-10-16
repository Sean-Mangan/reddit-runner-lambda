import csv
import random
import time
from pprint import pprint

from constants import NSFW_ENDPOINT_FILE, TERM_FILE, SFW_ENDPOINT_FILE, TIME_TO_RUN
from random_utils import get_random_terms
from reddit_utils import get_reddit_auth, search_subreddits
from s3_utils import get_json, upload_json


def main(*args, **kwargs):
    """
    Lambda main function that will attempt to query for as many nsfw subreddits as possible
    1. Get all search terms from s3
    2. Get all the current subreddits found from s3
    3. Query the reddit api for each term from step 1
    4. Filter out the results to only get nsfw subreddits
    5. Save all of those subreddits to the file found in step 2
    """

    # These are the most up to date endpoints and search terms available
    search_terms = get_json(TERM_FILE)["terms"] + get_random_terms(300)

    # This token is valid for 24h
    access_token = get_reddit_auth()

    # Hold onto all the found nsfw subs
    nsfw_subreddits = set()
    sfw_subreddits = set()

    # Set the timeout if the lambda is about to expire
    timeout = time.time() + TIME_TO_RUN

    # Add none to terms since we always want a generic search (get the 5000 most popular subreddits)
    for term in [None] + search_terms:

        # If the lambda is about to expire, just break so the files can be saved
        if time.time() > timeout:
            break

        # Filter out all subreddits that don't meet certain criteria
        def _filter_conditions(sub):
            return all([
                sub["data"]["subreddit_type"] == "public",
                sub["data"]["subscribers"] or 0 >= 10000
            ])

        # Make sure each found sub reddit is publicly available
        found_subreddits = search_subreddits(access_token, query=term)
        public_subreddits = list(filter(_filter_conditions, found_subreddits))

        # Sort each sub into nsfw and sfw
        nsfw_found_endpoints = [sub["data"]["url"] for sub in public_subreddits if sub["data"]["over18"]]
        sfw_found_endpoints = [sub["data"]["url"] for sub in public_subreddits if not sub["data"]["over18"]]
        nsfw_subreddits.update(set(nsfw_found_endpoints))
        sfw_subreddits.update(set(sfw_found_endpoints))

    # Finally upload the results to the json file for the next run
    upload_json({"endpoints": [endpoint for endpoint in nsfw_subreddits]}, NSFW_ENDPOINT_FILE)
    upload_json({"endpoints": [endpoint for endpoint in sfw_subreddits]}, SFW_ENDPOINT_FILE)