from rest_framework import serializers 
from rest_framework.fields import ListField
from .models import *

# ============= Serializers that corresponds to Model objects ===================
# ===============================================================================
class GroupChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChat
        fields = ['title', 'users']

class GroupChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChatMessage
        fields = ['user', 'room', 'timestamp', 'content']