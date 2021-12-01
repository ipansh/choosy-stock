import pandas as pd
import requests

from datetime import datetime
import time

class response_getter():

    def __init__(self):

        """ Base class with a couple of functions that return basic info.
        """

    def unix_to_date(unix_timestamp):
        ts = int(unix_timestamp)
        return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')

    def get_json_response(ticker, url, KEY):
        querystring = {"symbol":ticker,"region":"US"}

        headers = {
                  'x-rapidapi-host': "yh-finance.p.rapidapi.com",
                  'x-rapidapi-key': KEY
                  }

        return requests.request("GET", url, headers=headers, params=querystring).json()
