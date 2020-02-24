from django.contrib import admin
from django.contrib.admin import widgets
from django.utils.translation import gettext_lazy as _

from solo.admin import SingletonModelAdmin

from .fields import ProcessDefinitionField
from .forms import ActivitiConfigForm, get_process_definition_choices
from .models import ActivitiConfig


@admin.register(ActivitiConfig)
class ActivitiConfigAdmin(SingletonModelAdmin):
    form = ActivitiConfigForm
    fieldsets = (
        (None, {"fields": ("root_url", "enterprise", "tenant"),}),
        (_("Auth"), {"fields": ("basic_auth_username", "basic_auth_password"),}),
    )


class ActivitiFieldsMixin:
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if isinstance(db_field, ProcessDefinitionField):
            kwargs.update(
                {
                    "widget": widgets.AdminRadioSelect(),
                    "choices": get_process_definition_choices(),
                }
            )

        return super().formfield_for_dbfield(db_field, request, **kwargs)
