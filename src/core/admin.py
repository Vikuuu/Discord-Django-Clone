"""
Admin configurations for core applications.
"""

from django.contrib import admin
from core.models import UserAccount

admin.site.register(UserAccount)
