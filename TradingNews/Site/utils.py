from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate
from django.core.cache import cache
from .models import Follows
import requests
import json

class AlphaVantage:
    def __init__(self, key):
        self.key = key
    
    # input: string
    # output: json
    # description: 
    #   returns overview data of a symbol and store the data 
    #   in cache if it's not already stored
    def overview(self, symbol):
        if cache.get(f'Overview_{symbol}'):
            return cache.get(f'Overview_{symbol}')

        resp = requests.get(
            f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={self.key}'
        )

        data = self._http_error(resp)

        cache.set(f'Overview_{symbol}', data)

        return data

    # input: string
    # output: json
    # description:
    #   returns quote data of a symbol and store the data
    #   in cache if it's not already stored
    def quote(self, symbol):
        if cache.get(f'Quote_{symbol}'):
            return cache.get(f'Quote_{symbol}')

        resp = requests.get(
            f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.key}'
        )

        data = self._http_error(resp).get('Global Quote')

        cache.set(f'Quote_{symbol}', data)

        return data

    # input: string, string
    # output: json
    # description:
    #   return intraday data of a symbol
    def intraday(self, symbol, interval):
        resp = requests.get(
            f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={self.key}'
        )

        return self._json_error(resp)

    # input: string
    # output: json
    # description:
    #   returns end point of a keyword and store the data
    #   in cache if it's not already stored
    def end_point(self, keyword):
        # if keyword is longer than 5 it's not a stock symbol so return 0
        if len(keyword) > 5:
            return 0

        if cache.get(f'EndPoint_{keyword}'):
            return cache.get(f'EndPoint_{keyword}')

        resp = requests.get(
            f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={self.key}"
        )

        data = self._json_error(resp)

        # set the timeout of the cache longer because end points are less likely to change
        cache.set(f'EndPoint_{keyword}', data, 86400)

        return data

    # input: response
    # output: json
    # description: 
    #   error checking for alpha vantage requests.
    #   errors will be raise with Http404
    def _http_error(self, response):
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
    def _json_error(self, response):
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

