import asyncio
import logging
import itertools
import pathlib 
from PIL import Image
import subprocess

from monolith.infrastructure import execute_infrastructure
from resource.resource_queue import SimpleResourceQueue
from resource.providers.from_iterable import ProviderFromIterable
from resource.providers.fs_via_http import FsViaHttpProvider
from resource.providers.mixins import defaults_mixin
from resource.providers.periodic import PeriodicEventResourceProvider

logging.basicConfig(level=logging.INFO)


def is_image(path: pathlib.Path) -> bool:
    try:
        im = Image.open(path)
        im.verify()
    except Exception:
        return False
    return True


async def is_video(path: pathlib.Path):
    process = await asyncio.subprocess.create_subprocess_exec(
        "ffprobe", "-loglevel", "error", "-show_entries", "stream=codec_type", "-of", "default=nw=1", path,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    )
    result = await process.communicate()
    if process.returncode != 0:
        return False
    return "codec_type=video\n" in result[0].decode()


class MemeProvider(
    FsViaHttpProvider,
    defaults_mixin(default_tag="meme", defaults={"minimal_display_time": 5000.})):
    pass

class DisplayFoodStatusEventProvider(
    PeriodicEventResourceProvider,
    defaults_mixin(default_tag="display_status", defaults={"minimal_display_time": 30000.})
):
    pass

if __name__ == "__main__":
    queue = SimpleResourceQueue(10)
    asyncio.run(execute_infrastructure(queue, 
        (
            MemeProvider(queue=queue, interval=10., filetype=is_image, directory="/home/janczarknurek/not_work/www/memy/", url_prefix="http://localhost:2222/"),
            # make_provider_http(queue, 30., "commercial", "/mnt/nfs/youtube.com", "http://internet.www/youtube.com/", filetype=is_video),
            # UrlResourceProvider(queue, 5., (
            #     ("ser", "http://czyjestser.www/ser.txt"),
            # )),
            ProviderFromIterable(queue=queue, interval=5., event_tag="status", events=itertools.cycle(
                ({"ser": s} for s in ("Otóż TAK!!!", "Już prawie nie ma, @Piotr kup ser", "SER SIĘ SKOŃCZYŁ!!!!!!!!!!!!1111111jedenjeden"))
            )),
            DisplayFoodStatusEventProvider(queue=queue, interval=31.11),
        )
    ))
