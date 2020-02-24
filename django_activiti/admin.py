from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from solo.admin import SingletonModelAdmin

from .forms import ActivitiConfigForm
from .models import ActivitiConfig


@admin.register(ActivitiConfig)
class ActivitiConfigAdmin(SingletonModelAdmin):
    form = ActivitiConfigForm
    fieldsets = (
        (None, {"fields": ("root_url", "enterprise", "tenant"),}),
        (_("Auth"), {"fields": ("basic_auth_username", "basic_auth_password"),}),
    )
