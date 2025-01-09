from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CustomUser, Debt
from unfold.admin import ModelAdmin


class CustomGroupAdmin(ModelAdmin):
    search_fields = ['name']
    ordering = ['name']
    filter_horizontal = ['permissions']


class CustomUserAdmin(ModelAdmin):
    list_display = ['username', 'email', 'is_shop_owner', 'is_active']
    list_filter = ['is_shop_owner', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'is_shop_owner')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'phone_number', 'is_shop_owner'),
        }),
    )
    filter_horizontal = ['groups', 'user_permissions']


class DebtAdmin(ModelAdmin):
    list_display = ['customer', 'creditor', 'amount', 'created_at', 'due_date', 'is_paid']
    list_filter = ['is_paid', 'due_date']
    readonly_fields = ['created_at']
    search_fields = ['customer__username', 'creditor__username']

    class Meta:
        app_label = 'Core'


admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Debt, DebtAdmin)