from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from apps.accounts.forms import UserChangeForm, UserCreationForm
from apps.accounts.models import User, OtpCode


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "phone_number", "is_admin"]
    list_filter = ["is_admin"]
    readonly_fields = ['last_login']
    fieldsets = [
        (None, {"fields": ["email", "phone_number", "full_name", "password"]}),
        ("Permissions",
         {"fields": ["is_admin", "is_active", "is_superuser", "last_login", "groups", "user_permissions"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (None, {"classes": ["wide"], "fields": ["phone_number", "email", "full_name", "password1", "password2"], },),
    ]
    search_fields = ["email", "full_name"]
    ordering = ["full_name"]
    filter_horizontal = ['groups', 'user_permissions']


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ["phone_number", "code", "created_at"]
