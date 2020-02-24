"""
Public Python API to interact with Activiti.
"""
from typing import List

from .activiti_models import ProcessDefinition, factory
from .client import get_client_class


def get_process_definitions() -> List[ProcessDefinition]:
    client = get_client_class()()

    response = client.get(
        "repository/process-definitions",
        {"tenantId": client.config.tenant, "sort": "key", "order": "asc",},
    )
    assert response["size"] == response["total"], "Pagination not yet implemented"
    return factory(ProcessDefinition, response["data"])
