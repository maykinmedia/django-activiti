from dataclasses import dataclass
from typing import List, Union

from .types import JSONObject
from .utils import underscoreize


def factory(model: type, data: Union[JSONObject, List[JSONObject]]) -> type:
    _is_collection = isinstance(data, list)

    known_kwargs = list(model.__annotations__.keys())

    def _normalize(kwargs: dict):
        to_keep = {
            key: value
            for key, value in underscoreize(kwargs).items()
            if key in known_kwargs
        }
        return to_keep

    if not _is_collection:
        data = [data]

    instances = [model(**_normalize(_raw)) for _raw in data]

    if not _is_collection:
        instances = instances[0]
    return instances


@dataclass
class ProcessDefinition:
    id: str
    url: str
    key: str
    name: str
    version: int
    description: str
    category: str
    deployment_id: str
    deployment_url: str
    resource: str
    start_form_defined: bool
    suspended: bool
    tenant_id: str

    def __str__(self):
        return f"{self.name} (v{self.version})"
