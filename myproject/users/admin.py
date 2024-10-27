from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Payment

admin.site.register(Payment)

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
