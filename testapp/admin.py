from django.contrib import admin

from django_activiti.admin import ActivitiFieldsMixin

from .models import Activiti


@admin.register(Activiti)
class ActivitiAdmin(ActivitiFieldsMixin, admin.ModelAdmin):
    pass
