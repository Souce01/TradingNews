from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Follows
from .forms import SignUpModelForm, LoginModelForm
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
    if request.user.is_authenticated:
        raise Http404("Already authenticated. Sign out to create an account!")

    form = SignUpModelForm()
    if request.method == 'POST':
        form = SignUpModelForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            dj_login(request, user)
            return redirect('Site:index')
    return render(request, 'Site/sign-up.html', {"form": form})

def login(request):
    if request.user.is_authenticated:
        raise Http404("Already authenticated. Sign out to login on another account!")

    form = LoginModelForm()
    if request.method == 'POST':
        form = LoginModelForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                dj_login(request, user)
                return redirect('Site:index')

    return render(request, 'Site/login.html', {"form": form})

def logout(request):
    dj_logout(request)
    return redirect('Site:index')


def company(request, symbol, filter='relevancy', pageNb=1):
    newsapi = NewsApiClient(api_key=NewsApi_Key)
    ctx = {'page': pageNb, 'filter': filter, 'followed': False}

    if request.user.is_authenticated:
        if Follows.objects.filter(user=request.user, symbol=symbol):
            ctx.update({'followed': True})

    """
    #! for testing purposes only.
    data = open('C:/Users/alexandre/Desktop/project/TradingNews/TradingNews/Site/testingIBM.json')
    company = json.load(data)
    ctx.update({'company': company})
    data.close()

    data = open('C:/Users/alexandre\Desktop\project\TradingNews\TradingNews\Site/testingEndpoint.json')
    endPoint = json.load(data)
    ctx.update({'endPoint': endPoint['Global Quote']})
    data.close()
    """
    # restricted to 5 api calls per minute and 500 per day. So for tesing sake I'll use a json file for development
    resp = requests.get(
        f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol.upper()}&apikey={AlphaVantage_Key}'
    )
    company = resp.json()

    if company.get("note", "") != "":
        raise Http404("api call limit reached")
    
    if len(company) == 0:
        raise Http404("invalid symbol")

    ctx.update({'company': company})

    resp = requests.get(
        f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol.upper()}&apikey={AlphaVantage_Key}'
    )
    endPoint = resp.json()

    if endPoint.get("note", "") != "":
        raise Http404("api call limit reached")

    # using .get() here because otherwise django will raise a KeyError before other Http404 errors
    ctx.update({'endPoint': endPoint.get('Global Quote')})

    # if the filter in the request is not in the valid list raise 404 
    if filter not in validFilter:
        raise Http404("error, invalid filter")
    
    articles = newsapi.get_everything(
        q=f"{company['Name']} AND {company['Symbol']}", language='en', sort_by=filter, page=pageNb)
    ctx.update({'articles': articles})

    return render(request, 'Site/company.html', ctx)

def watchlist(request, filter='relevancy', pageNb=1):
    if not request.user.is_authenticated:
        raise Http404("Have to be logged in to view this page!")

    followed = Follows.objects.filter(user=request.user)
    return render(request, 'Site/watchlist.html')

def chartData(request, symbol, interval):
    if request.method == 'GET':
        symbol = symbol.upper()
        validInterval = ['1min', '5min', '15min', '30min', '60min']

        # will return an error if the time interval is not in the valid time interval list
        if interval not in validInterval:
            return JsonResponse({'status': False, 'message': 'Invalid time'}, status=400, safe=False)

        resp = requests.get(
            f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={AlphaVantage_Key}'
        )

        if resp.status_code != 200:
            # invalid request error response
            return JsonResponse({'status': False, 'message': 'bad request'}, status=400, safe=False)

        data = resp.json()

        if data.get("Error Message", "") != "":
            return JsonResponse({'status': False, 'message': 'Invalid symbol'}, status=400, safe=False)

        return JsonResponse(data, status=200, safe=False)


def searchEndpoint(request, keyword):
    if request.method == 'GET':
        resp = requests.get(
            f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={AlphaVantage_Key}"
        )

        if resp.status_code != 200:
            # invalid request error response
            return JsonResponse({'status': False, 'message': 'bad request'}, status=400, safe=False)

        data = resp.json()

        if data.get("Error Message", "") != "":
            # invalid keyword response
            return JsonResponse({'status': False, 'message': 'Invalid keyword'}, status=400, safe=False)
        
        return JsonResponse(data, status=200, safe=False)

def follow(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            symbol = json.loads(request.body).get("symbol", "")
            if symbol != "":
                if Follows.objects.filter(user=request.user, symbol=symbol):
                    Follows.objects.get(user=request.user,
                                        symbol=symbol).delete()
                    return JsonResponse({'followed': False, 'symbol': symbol})
                else:
                    follow = Follows(user=request.user,
                                     symbol=symbol)
                    follow.save()
                    return JsonResponse({'symbol': symbol, 'user': request.user.id, 'followed': True})
            return JsonResponse({'status': False})
