from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from .models import Follows
from .forms import SignUpModelForm, LoginModelForm
from newsapi import NewsApiClient
from .utils import AlphaVantage
import json
import os

NEWSAPI_KEY = os.environ.get('NEWSAPI_KEY')
ALPHAVANTAGE_KEY = os.environ.get('ALPHAVANTAGE_KEY')

validFilter = ['popularity', 'relevancy', 'publishedAt']

# input: request
# output: rendered page
# description: renders the index page
def index(request):
    newsapi = NewsApiClient(api_key=NEWSAPI_KEY)
    ctx = {}

    articles = newsapi.get_top_headlines(
        language='en',
        category='business',
        country='us'
    )
    
    # removing the first 3 articles and placing them in healines 
    # because they will be rendered from a previous template
    # so I have to use different variables
    headlines = articles['articles'][:3]
    del articles['articles'][:3]
    
    ctx.update({'headlines': headlines, 'articles': articles})

    if request.user.is_authenticated:
        alphaVantage = AlphaVantage(key=ALPHAVANTAGE_KEY)
        # returns user's followed list with quote information
        followedList = Follows.get_user_follows_quote(
            user=request.user, alphaVantage=alphaVantage)

        ctx.update({'followedList': followedList})

    return render(request, 'Site/index.html', ctx)

# input: request
# output: 
#   -get: rendered page
#   -post: redirection
# description: 
#   -get: renders sign-up page
#   -post: creates, authenticate and login a new user from form data
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

# input: request
# output:
#   -get: rendered page
#   -post: redirection
# description:
#   -get: renders login page
#   -post: authenticate and login user from form data
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

# input: request
# output: redirection
# description: logout the user
def logout(request):
    dj_logout(request)
    return redirect('Site:index')

# input: request, string, string, int
# output: rendered page
# description:
#   view for the company page
#   shows in depth data and articles on the selected stock
def company(request, symbol, filter='relevancy', pageNb=1):
    # if the filter in the request is not in the valid list raise 404
    if filter not in validFilter:
        raise Http404("error, invalid filter")

    newsapi = NewsApiClient(api_key=NEWSAPI_KEY)
    alphaVantage = AlphaVantage(key=ALPHAVANTAGE_KEY)
    symbol = symbol.upper()

    # Initiate the context variables
    ctx = {'page': pageNb, 'filter': filter, 'followed': False}

    if request.user.is_authenticated:
        # checks if the user is following the stock of the current page
        if Follows.objects.filter(user=request.user, symbol=symbol):
            ctx.update({'followed': True})
        
        # returns user's followed list with quote information
        followedList = Follows.get_user_follows_quote(
            user=request.user, alphaVantage=alphaVantage)

        ctx.update({'followedList': followedList})

    company = alphaVantage.overview(symbol=symbol)
    quote = alphaVantage.quote(symbol=symbol).get('Global Quote')
    
    articles = newsapi.get_everything(
        q=f'"{company["Name"]}" AND {company["Symbol"]}', language='en', sort_by=filter, page=pageNb)
    
    ctx.update({'articles': articles, 'quote': quote, 'company': company})

    return render(request, 'Site/company.html', ctx)

# input: request, string, int
# output: rendered page
# description:
#   view for the watchlist
#   shows all articles related to user's followed list
@login_required
def watchlist(request, filter='relevancy', pageNb=1):
    # if the filter in the request is not in the valid list raise 404
    if filter not in validFilter:
        raise Http404("error, invalid filter")

    newsapi = NewsApiClient(api_key=NEWSAPI_KEY)
    alphaVantage = AlphaVantage(key=ALPHAVANTAGE_KEY)
    ctx = {'page': pageNb, 'filter': filter}

    followedList = Follows.get_user_follows_quote(
        user=request.user, alphaVantage=alphaVantage)

    if followedList is not None:
        # initiate array used for creating the query
        followed = []
        
        # for every followed stock by the user add the symbol to the followed array
        for obj in Follows.objects.filter(user=request.user):
            followed.append(f'({obj.symbol} AND "{obj.name}")')
        # Creating the querry from the followed array by joining it with a OR seperator
        query = ' OR '.join(followed)

        articles = newsapi.get_everything(q=query, language='en', sort_by=filter, page=pageNb)
        ctx.update({'articles': articles, 'followedList': followedList})

    #TODO message when you don't have any followed

    return render(request, 'Site/watchlist.html', ctx)

# input: request, string, string
# output: json
# description: 
#   sends json response of symbol's chart data
def chartData(request, symbol, interval):
    if request.method == 'GET':
        alphaVantage = AlphaVantage(key=ALPHAVANTAGE_KEY)
        symbol = symbol.upper()
        validInterval = ['1min', '5min', '15min', '30min', '60min']

        # will return an error if the time interval is not in the valid time interval list
        if interval not in validInterval:
            return JsonResponse({'message': 'Invalid time'}, status=400, safe=False)

        data = alphaVantage.intraday(symbol=symbol, interval=interval)

        return JsonResponse(data, safe=False)

# input: request, string
# output: json
# description:
#   returns stocks related to keyword
#   used for a search bar
def searchEndpoint(request, keyword):
    if request.method == 'GET':
        alphaVantage = AlphaVantage(key=ALPHAVANTAGE_KEY)
        data = alphaVantage.end_point(keyword=keyword)

        return JsonResponse(data, safe=False)

# input: request
# output: json
# description:
#   this view will add or remove a stock from the user's followed list
@login_required
def follow(request):
    if request.method == 'POST':
        req     = json.loads(request.body)
        symbol  = req.get("symbol", "")
        name    = req.get("name", "")
        if symbol != "" and name != "":
            # if the user already follows the stock, remove it from the database
            # and send confirmation to the front-end
            if Follows.objects.filter(user=request.user, symbol=symbol):
                Follows.objects.get(user=request.user,
                                    symbol=symbol).delete()
                return JsonResponse({'followed': False, 'symbol': symbol, 'name': name}, safe=False)
            else:
                follow = Follows(user=request.user,
                                 symbol=symbol, name=name)
                follow.save()
                return JsonResponse({'symbol': symbol, 'name': name, 'user': request.user.id, 'followed': True}, safe=False)
        return JsonResponse({'status': False}, safe=False)
