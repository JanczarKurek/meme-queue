import typing

from resource.resource_provider import TimeBasedResourceProvider


class ProviderFromIterable(TimeBasedResourceProvider):
        def __init__(self, *, event_tag:str, events: typing.Iterable, **kwargs):
            self._default_tag = event_tag
            self._events = events
            super().__init__(**kwargs)
        
        def default_tag(self) -> str:
            return self._default_tag
        
        async def next_resource(self):
            try:
                return {"payload": next(self._events)}
            except StopIteration:
                return None
