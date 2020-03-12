from django.core.exceptions import ValidationError

import pytest
import requests_mock

from django_activiti.models import ActivitiConfig


@pytest.mark.django_db
def test_config_model_url_ok():
    config = ActivitiConfig.get_solo()
    config.enabled = True

    with requests_mock.Mocker() as m:
        m.get(
            "https://activiti.example.com/activiti-app/api/management/engine",
            status_code=200,
        )

        config.clean()


@pytest.mark.django_db
def test_config_model_url_not_ok():
    config = ActivitiConfig.get_solo()
    config.enabled = True

    with requests_mock.Mocker() as m:
        m.get(
            "https://activiti.example.com/activiti-app/api/management/engine",
            status_code=401,
        )

        with pytest.raises(ValidationError):
            config.clean()
