from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Profile
from django.utils.translation import gettext_lazy as _

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'role', 'wallet_balance', 'is_premium', 'is_staff')

    list_filter = ('role', 'is_staff', 'is_active')

    list_editable = ('role', 'wallet_balance')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        #(_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Financial & Subscription'), {
            'fields': ('wallet_balance', 'subscription_expires_at'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1','password2', 'role', 'is_staff', 'is_active'),
        }),
    )

    ordering = ('-date_joined',)
    search_fields = ('email',)

    @admin.display(boolean=True, description='Premium')
    def is_premium(self, obj):
        return obj.is_premium


admin.site.register(Profile)
