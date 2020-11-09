from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate
from django.core.cache import cache
from functools import wraps
from .models import Follows
import requests
import json


# decorator for caching the alphavantage data
def cache_data(function):
    def wrapper(*args, **kwargs):
        param = '_'.join(kwargs.values())
        query = f'{function.__name__}_{param}'
        if cache.get(query):
            return cache.get(query)

        data = function(*args, **kwargs)

        cache.set(query, data)
        return data
    return wrapper


def json_error(function):
    def wrapper(*args, **kwargs):
        response = function(*args, **kwargs)

        if response.status_code != 200:
            return JsonResponse({'message': 'bad request'}, status=400, safe=False)

        data = response.json()

        # The api returns a variable called note if the max numbers of calls are made to the api
        if data.get("Note"):
            return JsonResponse({'message': 'api call limit reached'}, status=400, safe=False)

        # The api returns an empty json file or an error message if the symbol has no match
        if len(data) == 0 or data.get("Error Message"):
            return JsonResponse({'message': 'Invalid symbol'}, status=400, safe=False)

        return data
    """
     change the name of the wrapper function to the parameter function name because
     this decorator could be chained with cache_data and it needs to store the function name
     of the first function to properly store data.
    """
    wrapper.__name__ = function.__name__
    return wrapper


def http_error(function):
    def wrapper(*args, **kwargs):
        response = function(*args, **kwargs)
        if response.status_code != 200:
            raise Http404("internal error")

        data = response.json()

        # The api returns a variable called note if the max numbers of calls are made to the api
        if data.get("Note"):
            raise Http404("api call limit reached")

        # The api returns an empty json file or an error message if the symbol has no match
        if len(data) == 0 or data.get("Error Message"):
            raise Http404("invalid symbol")

        return data
    """
     change the name of the wrapper function to the parameter function name because
     this decorator could be chained with cache_data and it needs to store the function name
     of the first function to properly store data.
    """
    wrapper.__name__ = function.__name__
    return wrapper

#! WHEN USING ANY FUNCTION THAT USES THE CACHE_DATA DECORATOR ALWAYS USE 
#! KEYWORD ARGUMENTS OTHERWISE THE DATA WILL NOT BE CACHED
class AlphaVantage:
    def __init__(self, key):
        self.key = key
    
    # input: string
    # output: json
    # description: 
    #   returns overview data of a symbol and store the data 
    #   in cache if it's not already stored
    @cache_data
    @http_error
    def overview(self, symbol):
        resp = requests.get(
            f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={self.key}'
        )
        return resp

    # input: string
    # output: json
    # description:
    #   returns quote data of a symbol and store the data
    #   in cache if it's not already stored
    @cache_data
    @http_error
    def quote(self, symbol):
        resp = requests.get(
            f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.key}'
        )

        return resp

    # input: string, string
    # output: json
    # description:
    #   return intraday data of a symbol
    @json_error
    def intraday(self, symbol, interval):
        resp = requests.get(
            f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={self.key}'
        )

        return resp

    # input: string
    # output: json
    # description:
    #   returns end point of a keyword and store the data
    #   in cache if it's not already stored
    @cache_data
    @json_error
    def end_point(self, keyword):
        # if keyword is longer than 5 it's not a stock symbol so return 0
        if len(keyword) > 5:
            return 0

        resp = requests.get(
            f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={self.key}"
        )

        return resp


    """
    # input: response
    # output: json
    # description: 
    #   error checking for alpha vantage requests.
    #   errors will be raise with Http404
    def __http_error(self, response):
        if response.status_code != 200:
            raise Http404("internal error")

        data = response.json()

        # The api returns a variable called note if the max numbers of calls are made to the api
        if data.get("Note"):
            raise Http404("api call limit reached")

        # The api returns an empty json file or an error message if the symbol has no match
        if len(data) == 0 or data.get("Error Message"):
            raise Http404("invalid symbol")

        return data

    # input: response
    # output: json
    # description:
    #   error checking for alpha vantage requests.
    #   errors will sent with JsonResponse
    def __json_error(self, response):
        if response.status_code != 200:
            return JsonResponse({'message': 'bad request'}, status=400, safe=False)

        data = response.json()

        # The api returns a variable called note if the max numbers of calls are made to the api
        if data.get("Note"):
            return JsonResponse({'message': 'api call limit reached'}, status=400, safe=False)

        # The api returns an empty json file or an error message if the symbol has no match
        if len(data) == 0 or data.get("Error Message"):
            return JsonResponse({'message': 'Invalid symbol'}, status=400, safe=False)

        return data

    """
