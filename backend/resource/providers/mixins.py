import typing

from resource.resource_provider import ResourceProvider


def defaults_mixin(default_tag: str, defaults: typing.Mapping[str, typing.Any]) -> type[ResourceProvider]:
    defaults = dict(defaults)
    class DefaultsMixin(ResourceProvider):
        def default_tag(self):
            return default_tag
        def defaults(self):
            return dict(defaults)
    return DefaultsMixin
