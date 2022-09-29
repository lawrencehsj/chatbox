from rest_framework import serializers 
from rest_framework.fields import ListField
from .models import *

# ============= Serializers that corresponds to Model objects ===================
# ===============================================================================
class FriendListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendList
        fields = ['user','friends']

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['sender','receiver', 'is_active', 'timestamp']
