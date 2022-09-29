from django.urls import path
from . import api


#required app_name from new django version
app_name = 'groupchat'

urlpatterns = [
    path('api/gc/<int:id>', api.GroupChatDetailsList.as_view(), name="groupchat_details_list"), # endpoint2, tested
]