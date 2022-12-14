"""chatbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from chatbox.views import home_screen_view
from account.views import (
    register_view,
    login_view,
    logout_view,
    account_search_view,
)

from account.api import AccountList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name="login"), 
    path('home/', home_screen_view, name="home"), 
    path('logout/', logout_view, name="logout"), 
    path('register/', register_view, name="register"),
    path('account/', include('account.urls', namespace='account')), # namespace for url extension, account:view in html
    path('search/', account_search_view, name="search"),

    path('groupchat/', include('groupchat.urls', namespace='groupchat')),
    path('friend/', include('friend.urls', namespace='friend')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
