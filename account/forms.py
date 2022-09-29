from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account


class RegistrationForm(UserCreationForm):
    ''' 
    Creates UserCreationForm based on the following fields:
    1. username
    2. password
    3. confirm password
    '''
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2', )

    # normalise email fields, prepend 'clean' => 'clean_email'
    def clean_email(self):
        email = self.cleaned_data['email'].lower() # ['email'] here is html name attribute (register.html)
        try:
            # check if email exist in database
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            # if not then email can be used
            return email
        raise forms.ValidationError(f'Email {email} is already in use.')

    # check for username availability
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(f'Username {username} is already in use.')


class LoginForm(forms.ModelForm):
    ''' 
    Creates LoginForm based on the following fields:
    1. email
    2. password
    '''
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class EditAccountForm(forms.ModelForm):
    ''' 
    Creates EditAccountForm based on the following fields:
    1. username
    2. email
    3. profile image
    4. show email
    '''
    class Meta:
        model = Account
        fields = ('username', 'email', 'profile_image', 'show_email' )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError(f'Email {email} is already in use.')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(f'Username {username} is already in use.')

    # save the account upon commit
    def save(self, commit=True):
        account = super(EditAccountForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email'].lower()
        account.profile_image = self.cleaned_data['profile_image']
        account.show_email = self.cleaned_data['show_email']
        if commit:
            account.save()
        return account