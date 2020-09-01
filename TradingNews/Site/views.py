from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, JsonResponse
from django.contrib import messages
from .models import Company
from newsapi import NewsApiClient
from datetime import datetime
import requests
#! just for testing
import json

AlphaVantage_Key = '43RT6XRIMUZDJW8D'
NewsApi_Key = '69ed3f87e0a34481b5f2da1ab93fd45f'
validFilter = ['popularity', 'relevancy', 'publishedAt']
# all request will be in english and from the US for now

def index(request):
    return render(request, 'Site/index.html')

def signUp(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('Site:index')
    return render(request, 'Site/sign-up.html', {"form": form})


def company(request, symbol, filter='relevancy', pageNb=1):
    newsapi = NewsApiClient(api_key=NewsApi_Key)

    #! for testing purposes only.
    data = open('C:/Users/alexandre/Desktop/project/TradingNews/TradingNews/Site/testingIBM.json')
    company = json.load(data)
    data.close()

    data = open('C:/Users/alexandre\Desktop\project\TradingNews\TradingNews\Site/testingEndpoint.json')
    endPoint = json.load(data)
    data.close()

    # restricted to 5 api calls per minute and 500 per day. So for tesing sake I'll use a json file for development
    """
    resp = requests.get(
        'https://www.alphavantage.co/query?function=OVERVIEW&symbol={0}&apikey={1}'.format(symbol.upper(), AlphaVantage_Key)
    )
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

    return render(request, 'Site/company.html', { 'company': company, 'endPoint': endPoint['Global Quote'], 'articles': articles, 'page': pageNb, 'filter': filter})

def chartData(request, symbol, time):
    if request.method == 'GET':
        time = time.upper()
        symbol = symbol.upper()
        validTime = ['DAILY', 'WEEKLY', 'MONTHLY']

        # will return an error if the time interval is not in the valid time interval list
        if not any(element in time for element in validTime):
            return JsonResponse({'status': 'false', 'message': 'Invalid time'}, status=400, safe=False)

        resp = requests.get(
            f'https://www.alphavantage.co/query?function=TIME_SERIES_{time}&symbol={symbol}&apikey={AlphaVantage_Key}'
        )
        data = resp.json()

        # if the length of the api response is equal to one it means that there is only an error message
        # NewsApi does not respond with a 400 status when there is a bad request
        if resp.status_code != 200 or len(data) == 1:
            return JsonResponse({'status':'false', 'message':'Invalid symbol'}, status=400, safe=False)

        return JsonResponse(data, status=200, safe=False)
