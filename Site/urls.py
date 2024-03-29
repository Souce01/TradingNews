from django.urls import path
from . import views

app_name = 'Site'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signUp, name='sign-up'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('company/<str:symbol>', views.company, name='company'),
    path('company/<str:symbol>/<str:filter>', views.company, name='company-filter'),
    path('company/<str:symbol>/<str:filter>/<int:pageNb>', views.company, name='company-filter-page'),
    path('api/chartData/<str:symbol>/<str:interval>', views.chartData, name='api-chartData'),
    path('api/searchEndPoint/<str:keyword>', views.searchEndpoint, name='api-searchEndPoint'),
    path('api/follow', views.follow, name='api-follow'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('watchlist/<str:filter>', views.watchlist, name='watchlist-filter'),
    path('watchlist/<str:filter>/<int:pageNb>', views.watchlist, name='watchlist-filter-page')
]
