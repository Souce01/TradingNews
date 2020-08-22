from django.urls import path
from . import views

app_name = 'Site'
urlpatterns = [
    path('', views.index, name='index'),
    path('sign-up', views.signUp, name='sign-up'),
    path('company/<str:symbol>', views.company, name='company'),
    path('company/<str:symbol>/<str:filter>', views.company, name='company-filter'),
    path('company/<str:symbol>/<str:filter>/<int:pageNb>', views.company, name='company-filter-page')
]
