from django.db import models

from django_activiti.fields import ProcessDefinitionField


class Activiti(models.Model):
    process_definition = ProcessDefinitionField(blank=True)
