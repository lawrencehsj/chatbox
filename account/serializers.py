from rest_framework import serializers 
from rest_framework.fields import ListField
from .models import *

# ============= Serializers that corresponds to Model objects ===================
# ===============================================================================
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['pk','email', 'username', 'profile_image', 'is_superuser']