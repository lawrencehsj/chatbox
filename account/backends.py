from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# CHANGES TO BE MADE TO VARIABLES
class CaseInsensitiveModelBackend(ModelBackend):

    # override 
    '''
    This function serves to eliminate case sensitivity when dealing with account authentication.
    Source code referenced from https://codingwithmitch.com/courses/real-time-chat-messenger
    '''
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model() # get the model in settings.py (account.Account)
        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        try:
            # convert to case insensitive, and get user based on that
            case_insensitive_username_field = '{}__iexact'.format(user_model.USERNAME_FIELD) 
            user = user_model._default_manager.get(**{case_insensitive_username_field: username})
        except user_model.DoesNotExist:
            user_model().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user