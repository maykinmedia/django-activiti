from django.urls import reverse

import pytest

from django_activiti.models import ActivitiConfig


@pytest.mark.django_db
def test_enter_basic_auth(requests_mock, django_app, admin_user):
    config = ActivitiConfig.get_solo()
    config.enabled = True
    config.save()
    assert config.auth_header == ""
    django_app.set_user(admin_user)
    requests_mock.get(
        "https://activiti.example.com/activiti-app/api/management/engine",
        status_code=200,
    )
    admin_url = reverse("admin:django_activiti_activiticonfig_changelist")

    change_page = django_app.get(admin_url)

    change_page.form["basic_auth_username"] = "dummy"
    change_page.form["basic_auth_password"] = "secret"
    change_page.form.submit().follow()

    config.refresh_from_db()
    assert config.auth_header == "Basic ZHVtbXk6c2VjcmV0"

    auth = requests_mock.last_request.headers["Authorization"]
    assert auth == "Basic ZHVtbXk6c2VjcmV0"


@pytest.mark.django_db
def test_select_process_definition(requests_mock, django_app, admin_user):
    config = ActivitiConfig.get_solo()
    config.enabled = True
    config.save()

    django_app.set_user(admin_user)
    requests_mock.get(
        "https://activiti.example.com/activiti-app/api/repository/process-definitions",
        json={
            "total": 2,
            "size": 2,
            "data": [
                {
                    "id": "dummy:1",
                    "url": (
                        "https://activiti.example.com/activiti-app/api/repository/"
                        "process-definitions/dummy:1"
                    ),
                    "key": "dummy",
                    "name": "Dummy",
                    "version": 1,
                    "description": "",
                    "category": "",
                    "deploymentId": "123",
                    "deploymentUrl": "",
                    "resource": "foo.bpmn",
                    "startFormDefined": False,
                    "suspended": False,
                    "tenantId": "tenant_1",
                },
                {
                    "id": "dummy:2",
                    "url": (
                        "https://activiti.example.com/activiti-app/api/repository/"
                        "process-definitions/dummy:2"
                    ),
                    "key": "dummy",
                    "name": "Dummy",
                    "version": 2,
                    "description": "",
                    "category": "",
                    "deploymentId": "456",
                    "deploymentUrl": "",
                    "resource": "foo.bpmn",
                    "startFormDefined": False,
                    "suspended": False,
                    "tenantId": "tenant_1",
                },
            ],
        },
    )
    admin_url = reverse("admin:testapp_activiti_add")
    add_page = django_app.get(admin_url)
    field = field = add_page.form["process_definition"]

    try:
        field.select("dummy:2")
    except Exception:
        pytest.fail("Missing option dummy:2")

    with pytest.raises(ValueError):
        field.select("foo")
