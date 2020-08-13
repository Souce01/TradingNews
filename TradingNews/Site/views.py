from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from django.contrib import messages
from .models import Company
from newsapi import NewsApiClient
from datetime import datetime
import requests
#just for testing
import json

AlphaVantage_Key = '43RT6XRIMUZDJW8D'
NewsApi_Key = '69ed3f87e0a34481b5f2da1ab93fd45f'
validFilter = ['popularity', 'relevancy', 'publishedAt']
# all request will be in english and from the US for now

def index(request):
    return render(request, 'Site/index.html')


def company(request, symbol, filter='relevancy', pageNb=1):
    newsapi = NewsApiClient(api_key=NewsApi_Key)

    #for testing purposes only.
    data = open('C:/Users/alexandre/Desktop/project/TradingNews/TradingNews/Site/testingIBM.json')
    company = json.load(data)
    data.close()

    # restricted to 5 api calls per minute and 500 per day. So for tesing sake I'll use a json file for development
    """
    resp = requests.get(
        'https://www.alphavantage.co/query?function=OVERVIEW&symbol={0}&apikey={1}'.format(symbol.upper(), AlphaVantage_Key))
    company = resp.json()

    # if the request is invalid or the json is empty because the symbol is invalid raise 404
    if resp.status_code != 200 or len(company) == 0:
        raise Http404("error")
    """

    # if the filter in the request is not in the valid list raise 404 
    if not any(element in filter for element in validFilter):
        raise Http404("error")
    
    articles = newsapi.get_everything(
        q="{0} AND {1}".format(company['Name'], company['Symbol']), language='en', sort_by=filter, page=pageNb)

    return render(request, 'Site/company.html', { 'company': company, 'articles': articles, 'page': pageNb, 'filter': filter})
