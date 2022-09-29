import factory

from django.test import TestCase
from django.conf import settings
from django.core.files import File

from .models import *
from account.models import Account
from account.model_factories import AccountFactory

# Factory objects used for testing
class FriendListFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(AccountFactory)
    friends = factory.SubFactory(AccountFactory)
    class Meta:
        model = FriendList

class FriendRequestFactory(factory.django.DjangoModelFactory):
    sender = factory.SubFactory(AccountFactory)
    receiver = factory.SubFactory(AccountFactory)
    class Meta:
        model = FriendRequest