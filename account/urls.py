from django.urls import path

from account.views import (
	account_view,
	edit_account_view,
)

from account.api import AccountList
# from . import api

#required app_name from new django version
app_name = 'account'

urlpatterns = [
	path('<user_id>/', account_view, name="view"),
    path('<user_id>/edit/', edit_account_view, name="edit"),
    path('api/<int:pk>', AccountList.as_view(), name="account_details_list"), 
]