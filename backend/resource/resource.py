import dataclasses
import time
from typing import Any


@dataclasses.dataclass
class Resource:
    resource_tag: str  # Type of resource
    payload: Any  # Additional misc. data
    priority: int = 0  # More means more
    creation_time: float = dataclasses.field(default_factory=time.time)
    display_time: float = dataclasses.field(default_factory=time.time)  # When we want to display it.
    decay_time: float | None = None # Time after which the resource gets deprecated and should no longer be displayed

    def to_json(self) -> dict[str, Any]:
        return dataclasses.asdict(self)

    @classmethod
    def from_json(cls, j: dict):
        return Resource(**j)
