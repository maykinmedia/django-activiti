from django.core.exceptions import ValidationError
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
    tenant = models.CharField(
        _("tenant ID"), max_length=100, default="tenant_1", blank=True
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

        from .client import get_client_class

        client = get_client_class()(config=self)
        try:
            client.get("management/engine")
        except Exception as exc:
            raise ValidationError(
                _(
                    "Invalid API root '{root}'. Got error: {error} while checking the "
                    "management/engine endpoint."
                ).format(root=self.root_url, error=exc)
            )
