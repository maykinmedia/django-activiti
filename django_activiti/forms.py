import base64
from typing import Union

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ActivitiConfig


class ActivitiConfigForm(forms.ModelForm):
    basic_auth_username = forms.CharField(
        label=_("Username"),
        required=False,
        help_text=_("Username to authenticate against the Activiti/APS API."),
    )

    basic_auth_password = forms.CharField(
        label=_("Password"),
        required=False,
        help_text=_("Password to authenticate against the Activiti/APS API."),
        widget=forms.PasswordInput,
    )

    class Meta:
        model = ActivitiConfig
        fields = (
            "root_url",
            "enterprise",
            "tenant",
            "basic_auth_username",
            "basic_auth_password",
        )

    def __init__(self, *args, **kwargs):
        config = kwargs.get("instance")
        if config is not None:
            creds = self.set_creds_from_header(config)
            if creds is not None:
                kwargs.setdefault("initial", {})
                kwargs["initial"].update(creds)
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.set_basic_auth_header()
        config = super().save(*args, **kwargs)
        return config

    def set_basic_auth_header(self):
        username = self.cleaned_data.get("basic_auth_username")
        password = self.cleaned_data.get("basic_auth_password")
        if not (username and password):
            return

        basic_auth = f"{username}:{password}"
        b64 = base64.b64encode(basic_auth.encode()).decode()
        self.instance.auth_header = f"Basic {b64}"

    def set_creds_from_header(self, config: ActivitiConfig) -> Union[dict, None]:
        if not config.auth_header.startswith("Basic "):
            return

        prefix, b64 = config.auth_header.split(" ", 1)
        decoded = base64.b64decode(b64).decode()
        username, password = decoded.split(":", 1)
        return {
            "basic_auth_username": username,
            "basic_auth_password": password,
        }
