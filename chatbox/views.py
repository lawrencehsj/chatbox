from django.shortcuts import render
from django.conf import settings

# from groupchat.models import GroupChat

DEBUG = True

# Create your views here.
def home_screen_view(request):
    # create context var
    context = {}
    context['debug_mode'] = settings.DEBUG
    context['debug'] = DEBUG
    context['room_id'] = "1" # room_id here
    # context['title'] = GroupChat.__str__
    return render(request, "home.html", context)