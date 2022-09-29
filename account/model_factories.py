import factory

from django.test import TestCase
from django.conf import settings
from django.core.files import File

from .models import *

# Factory objects used for testing
class AccountFactory(factory.django.DjangoModelFactory):
    email = "test@test.com"
    username = "test"
    is_superuser = True
    # profile_image = null
    # show_email = models.BooleanField(default=True)
    # is_staff				= models.BooleanField(default=True)
    class Meta:
        model = Account

    