import json
import os
import time

import requests

from .temp_folder_handler import TempFolderHelper


class RedgifsApi:
    authentication_response = None
    token = ''
    expires = 0
    # -30 for a bit of extrabuffer
    expiry_duration = 3600 - 30
    auth_file_name = 'redgifs_auth.json'

    def __init__(self):
        pass

    def is_authenticated(self):
        return self.token != '' and self.expires > time.time()
        pass

    def authenticate(self):
        if self.try_local_authentication_file():
            return

        response = requests.get("https://api.redgifs.com/v2/auth/temporary")
        if response.status_code != 200:
            raise Exception("Redgifs authentication failed")

        item = response.json()
        self.authentication_response = item
        self.token = item['token']
        self.expires = time.time() + self.expiry_duration

        # save to disk
        file_path = os.path.join(TempFolderHelper.get_app_root_path(), self.auth_file_name)
        with open(file_path, 'w') as f:
            f.write(json.dumps(item))

    def try_local_authentication_file(self):
        root_path = TempFolderHelper.get_app_root_path()
        file_path = os.path.join(root_path, self.auth_file_name)

        if not os.path.exists(file_path):
            return False

        modified_time = os.path.getmtime(file_path)
        # get file modified time, if more than modified + expiry_duration then we return.
        if modified_time + self.expiry_duration < time.time():
            return False

        with open(file_path) as f:
            item = json.loads(f.read())
            self.authentication_response = item
            self.token = item['token']
            self.expires = modified_time + self.expiry_duration

        return True

    def get_and_download_video(self, resource):
        if not self.is_authenticated():
            self.authenticate()

        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(f"https://api.redgifs.com/v2/gifs/{resource}", headers=headers)
        if response.status_code != 200:
            raise Exception("Redgifs video information failed")

        item = response.json()
        if "errorMessage" in item:
            raise Exception(item["errorMessage"]["code"])

        urls = item["gif"]["urls"]
        url = urls.get('hd') if urls.get('hd') else urls.get('sd')
        video_response = requests.get(url, stream=True, headers=headers)
        if video_response.status_code == 200:
            video_path = os.path.join(TempFolderHelper.get_temp_folder_path(), f"{resource}.mp4")
            with open(video_path, "wb") as f:
                for chunk in video_response.iter_content(chunk_size=1024):
                    f.write(chunk)
            return video_path
        else:
            print("Failed to download")
            return False
