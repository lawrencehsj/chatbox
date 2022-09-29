from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account


class AccountAdmin(UserAdmin):
	list_display = ('email','username')
	search_fields = ('email','username')

    # null filter options
	filter_horizontal = () 
	list_filter = ()
	fieldsets = ()

admin.site.register(Account, AccountAdmin)