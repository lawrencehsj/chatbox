from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout # import
from django.conf import settings 

from account.forms import EditAccountForm, RegistrationForm, LoginForm
from account.models import Account

from friend.utils import *
from friend.models import FriendList, FriendRequest


def register_view(request, *args, **kwargs):
    """
    Register for user account page. Uses RegistrationForm in 'forms.py'.
    """	
    if request.user.is_authenticated: 
        return HttpResponse("You are already authenticated as " + str(request.user.email))

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save() # runs clean_email and clean_username
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home') 
    return render(request, 'account/register.html')

def logout_view(request):
    """
    Logout page. Auto redirect to login page.
    """	
    logout(request)
    return redirect("/")

def login_view(request, *args, **kwargs):
    """
    Login page. Uses LoginForm in 'forms.py'.
    """	
    # if user is logged in already, redirect to home page
    if request.user.is_authenticated: 
        return redirect("home")

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            account = authenticate(email=email, password=password)
            login(request, account)
            return redirect('home')
    return render(request, "account/login.html")


def account_view(request, *args, **kwargs):
    """
    Profile page.

    - Logic here is kind of tricky
        is_self (boolean)
            is_friend (boolean)
                -1: NO_REQUEST_SENT
                0: SENT_TO_YOU
                1: SENT_TO_THEM
    """
    # if user is not logged in, redirect to login page
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    user_id = kwargs.get("user_id")
    try:
        account = Account.objects.get(pk=user_id)
    except:
        return HttpResponse("Something went wrong.")
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.profile_image.url
        context['show_email'] = account.show_email

        try:
            friend_list = FriendList.objects.get(user=account)
        except FriendList.DoesNotExist:
            friend_list = FriendList(user=account)
            friend_list.save()
        friends = friend_list.friends.all()
        context['friends'] = friends # queryset

        # Define template variables
        is_self = True
        is_friend = False
        user = request.user
        
        # friend variables
        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value # range: ENUM -> friend/friend_request_status.FriendRequestStatus
        friend_requests = None
        
        # if not looking at own profile:
        if user.is_authenticated and user != account:
            is_self = False
            if friends.filter(pk=user.id):
                is_friend = True
            else:
                is_friend = False
                # CASE1: Request has been sent from THEM to YOU: FriendRequestStatus.SENT_TO_YOU
                if get_friend_request_or_false(sender=account, receiver=user) != False:
                    request_sent = FriendRequestStatus.SENT_TO_YOU.value
                    context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id #pk or id of FriendRequest model
                # CASE2: Request has been sent from YOU to THEM: FriendRequestStatus.SENT_TO_THEM
                elif get_friend_request_or_false(sender=user, receiver=account) != False:
                    request_sent = FriendRequestStatus.SENT_TO_THEM.value
                # CASE3: No request sent from YOU or THEM: FriendRequestStatus.NO_REQUEST_SENT
                else:
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value

        elif not user.is_authenticated:
            is_self = False

        else:
            try:
                friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
            except:
                pass
            
        # Set the template variables to the values
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL

        # friend variables
        context['request_sent'] = request_sent
        context['friend_requests'] = friend_requests

        return render(request, "account/account.html", context)


def edit_account_view(request, *args, **kwargs):
    """
    Edit account page. Uses EditAccountForm in 'forms.py'.
    """	
    # if user is not logged in, redirect to login page
    if not request.user.is_authenticated:
        return redirect("login")

    user_id = kwargs.get("user_id")
    account = Account.objects.get(pk=user_id)
    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit another person's account.")

    context={}
    if request.POST:
        form = EditAccountForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # delete the original profile image to be replaced (one image url only)
            account.profile_image.delete() 
            form.save()
            return redirect("account:view", user_id=account.pk)
    else:
        form = EditAccountForm(
            initial={
                "id": account.pk,
                "email": account.email, 
                "username": account.username,
                "profile_image": account.profile_image,
                "show_email": account.show_email,
            }
        )
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE # cap data upload size
    return render(request, "account/edit_account.html", context)


def account_search_view(request, *args, **kwargs):
    """
    Accounts search results page. 
    """	
    context = {}
    if request.method == "GET":
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            # icontains ignore case sensitive
            search_results = Account.objects.filter(email__icontains=search_query).filter(username__icontains=search_query).distinct()
            user = request.user
            accounts = [] # [(account1, True), (account2, False), ...]
            if user.is_authenticated:
                # get the authenticated users friend list
                auth_user_friend_list = FriendList.objects.get(user=user)
                for account in search_results:
                    accounts.append((account, auth_user_friend_list.is_mutual_friend(account)))
                context['accounts'] = accounts
            else:
                for account in search_results:
                    accounts.append((account, False)) 
                context['accounts'] = accounts
    return render(request, "account/search_results.html", context)
