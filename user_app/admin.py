from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Customer, Author


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    # readonly_fields = ('id', 'email', 'is_staff', 'is_active', 'date_joined', 'date_updated')
    list_display = ('id','email','is_staff', 'is_active', 'date_joined', 'date_updated',)
    list_filter = ('email', 'is_staff', )
    fieldsets = (
        (None, {'fields': ('email', 'password', )}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class CustomerAdminPanel(admin.ModelAdmin):
    # readonly_fields = ('id', 'user', 'session')
    list_display = ('id', 'user', 'session')

class AuthorAdminPanel(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'date_created',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Customer, CustomerAdminPanel)
admin.site.register(Author, AuthorAdminPanel)
