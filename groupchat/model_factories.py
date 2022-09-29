import factory

from django.test import TestCase
from django.conf import settings
from django.core.files import File

from .models import *
from account.model_factories import AccountFactory

# Factory objects used for testing
class GroupChatFactory(factory.django.DjangoModelFactory):
    title = "room name"
    users = factory.SubFactory(AccountFactory)

    class Meta:
        model = GroupChat

class GroupChatMessageFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(AccountFactory)
    room = factory.SubFactory(GroupChatFactory)
    timestamp = "2022-03-28T02:49:21.954171Z"
    content = 'hello there'
    class Meta:
        model = GroupChatMessage