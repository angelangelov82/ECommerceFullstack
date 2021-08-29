from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Account, UserProfile


# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')#Django admin site to show these fields of user data
    list_display_links = ('email', 'first_name', 'last_name')#these links allow you to see these fields as links and access user data page
    readonly_fields = ('last_login', 'date_joined')# we want these fields to be read only
    ordering = ('-date_joined',) # disending order of records

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius: 50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail','user', 'city', 'country')

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
