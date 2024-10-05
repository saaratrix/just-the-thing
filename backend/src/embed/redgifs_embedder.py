import re
import time

from .redgifs_api import RedgifsApi
from .temp_folder_handler import TempFolderHelper

redgifs_url_regex = re.compile(r"(https:\/\/)?(www\.|v3\.|v2\.)?redgifs\.com\/(watch|ifr)\/(?P<resource>\S+)", re.IGNORECASE)

class RedgifsEmbedder:
    verbose_logging = True

    api_handler = RedgifsApi()

    def __init__(self):
        pass

    def fetch_embed_resource(self, url):
        start_time = time.perf_counter()
        resource = self.get_resource(url)

        if resource is None:
            return False

        # check if file exists in temp folder and then return that.
        result = self.check_if_downloaded(resource)
        if result is not None:
            print(f"Found {resource} in temp folder.")
        else:
            result = self.api_handler.get_and_download_video(resource)

        end_time = time.perf_counter()
        print(f"Took {end_time - start_time} seconds to fetch redgifs video.")
        return result

    @staticmethod
    def check_if_downloaded(resource: str):
        file = f"{resource.lower()}.mp4"
        contains, path = TempFolderHelper.contains_file(file)

        if not contains:
            return None

        return path

    @staticmethod
    def get_resource(url):
        match = redgifs_url_regex.match(url)
        if match:
            return match.group('resource')

        return None