"""
Public Python API to interact with Activiti.
"""
import math
from concurrent import futures
from functools import partial
from typing import Any, Dict, List

from .activiti_models import ProcessDefinition, factory
from .client import get_client_class

MAX_WORKERS = 10


def _fetch_process_definitions(client, start: int = 0) -> Dict[str, Any]:
    response = client.get(
        "repository/process-definitions",
        {
            "tenantId": client.config.tenant,
            "sort": "key",
            "order": "asc",
            "start": start,
        },
    )
    return response


def get_process_definitions() -> List[ProcessDefinition]:
    client = get_client_class()()
    _fetcher = partial(_fetch_process_definitions, client)

    results = []
    # fetch first page, which gives info about total
    response = _fetcher()
    results += response["data"]
    total = response["total"]

    pages = math.ceil(total / response["size"])

    with futures.ThreadPoolExecutor(
        max_workers=max(pages - 1, MAX_WORKERS)
    ) as executor:
        starts = [response["size"] * page for page in range(1, pages)]
        responses = executor.map(_fetcher, starts)

    for response in responses:
        results += response["data"]

    assert len(results) == total, "Pagination processing went wrong"

    return factory(ProcessDefinition, results)
