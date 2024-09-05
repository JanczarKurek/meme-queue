from resource.resource_provider import TimeBasedResourceProvider


class PeriodicEventResourceProvider(TimeBasedResourceProvider):
        """Just emit some event type with no payload."""
    
        async def next_resource(self):
            return {"payload": None}
