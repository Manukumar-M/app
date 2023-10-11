from django.contrib import admin

# Register your models here.
from django.contrib.admin.views.main import ChangeList
from .models import CustomUser
from django.contrib import admin

class UserChangeList(ChangeList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_display = ['id', 'username', 'email', 'phone_number', 'web_terms', 'dataprocessing', 'subscription', 'created_date', 'modified_date']

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'phone_number', 'web_terms', 'dataprocessing', 'subscription', 'created_date', 'modified_date']
    search_fields = ['id', 'username', 'email', 'phone_number']
    list_filter = ['web_terms', 'dataprocessing', 'subscription']
    readonly_fields = ['created_date', 'modified_date']

    def get_changelist(self, request, **kwargs):
        return UserChangeList
    
    











