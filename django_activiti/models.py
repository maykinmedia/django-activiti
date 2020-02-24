from django.db import models
from django.utils.translation import gettext_lazy as _

from solo.models import SingletonModel


class ActivitiConfig(SingletonModel):
    """ configuration of Activiti service, including base url and credentials """

    root_url = models.URLField(
        _("activiti root"),
        help_text=_("Root URL where the Activiti API is deployed."),
        default="https://activiti.example.com/activiti-app/api",
    )
    auth_header = models.TextField(
        _("authorization header"),
        blank=True,
        help_text=_(
            "HTTP Authorization header value, required if the API is not open."
        ),
    )
    enterprise = models.BooleanField(
        _("is enterprise"),
        default=True,
        help_text=_(
            "Boolean indicating if the enterprise edition of Activiti is used. "
            "The enterprise edition has different API endpoints, which needs to be "
            "taken into account to start process instances or fetch the start form "
            "configuration."
        ),
    )

    class Meta:
        verbose_name = _("Activiti configuration")

    def __str__(self):
        return self.root_url

    def save(self, *args, **kwargs):
        # normalize URLs
        if not self.root_url.endswith("/"):
            self.root_url = f"{self.root_url}/"
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        # TODO: verify config is correct
