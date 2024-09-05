from pathlib import Path
import urllib

from resource.providers.fs import FsResourceProvider


class FsViaHttpProvider(FsResourceProvider):

    def __init__(self, *,  url_prefix: str, **kwargs):
        super().__init__(**kwargs)
        self._url_prefix = url_prefix
    
    def path_to_payload(self, path: Path):
        return urllib.parse.urljoin(self._url_prefix, path.name)
