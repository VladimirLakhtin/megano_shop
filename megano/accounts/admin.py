from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_full_name')
    list_select_related = ('profile', )

    def get_full_name(self, instance):
        return instance.profile.fullName
    get_full_name.short_description = 'Fullname'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
