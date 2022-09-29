import json
# from winreg import HKEY_PERFORMANCE_DATA
from django.http import JsonResponse, HttpResponse
from django.utils.translation import get_supported_language_variant #default Response
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, query

#rest api packages
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response #rest Response, better for development
from rest_framework import status

#packages for easier logic to handle CRUD
from rest_framework import generics
from rest_framework import mixins
# permissions
from rest_framework.permissions import IsAuthenticated

#package for appending querysets
from itertools import chain

from .models import *
from .serializers import *

