from django.db import models
from django.utils.translation import gettext_lazy as _

from .forms import ProcessDefinitionChoicesField


class ProcessDefinitionField(models.CharField):
    def __init__(self, *args, **kwargs):
        # See https://github.com/Activiti/Activiti/blob/develop/activiti-core/activiti-engine/
        # src/main/resources/org/activiti/db/create/activiti.postgres.create.engine.sql#L171
        # for the DB column size in activiti
        kwargs.setdefault("max_length", 64)
        kwargs.setdefault("help_text", _("ID of the process definition in Activiti"))
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {"form_class": ProcessDefinitionChoicesField}
        defaults.update(**kwargs)
        return super().formfield(**defaults)
