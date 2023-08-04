import dataclasses
import time
from typing import Any


@dataclasses.dataclass
class Resource:
    resource_tag: str  # Type of resource
    payload: Any  # Additional misc. data
    display_time: float  # When we want to display it.
    creation_time: float = dataclasses.field(default_factory=time.time())

    def to_json(self) -> dict[str, Any]:
        return dataclasses.asdict(self)
