from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
import uuid
from datetime import datetime


class CustomUser(AbstractUser):
    # Additional fields
    
    id = models.AutoField(primary_key=True)
    username = models.CharField(_('username'), max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True, null=True, blank=True)
    phone_number = models.IntegerField(_('phone_number'),unique=True, null=True, blank=True)
    password = models.CharField(_('password'), max_length=128, help_text=_("Use '[algo]$[salt]$[hexdigest]' or use the <a href='password/'>change password form</a>."))
    web_terms = models.BooleanField(default=False)
    dataprocessing = models.BooleanField(default=False)
    subscription = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    

    @property
    def web_terms_display(self):
        return "1" if self.web_terms else "0"

    @property
    def dataprocessing_display(self):
        return "1" if self.dataprocessing else "0"

    @property
    def subscription_display(self):
        return "1" if self.subscription else "0"

    def __str__(self):
            return self.username or self.email or self.phone_number

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_users_groups',
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of those groups.'),
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_users_permissions',
        help_text=_('Specific permissions for this user.'),
        related_query_name='user',
    )
    
    