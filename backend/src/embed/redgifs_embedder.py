# import os
import re
import time

# import requests
# from selenium.webdriver.common.by import By
# from seleniumwire import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager

from .redgifs_api import RedgifsApi
# from backend.src.embed.temp_folder_handler import TempFolderHelper

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

        result = self.api_handler.get_and_download_video(resource)
        end_time = time.perf_counter()
        print(f"Took {end_time - start_time} seconds to fetch redgifs video.")
        return result


    #     target_url = f"https://www.redgifs.com/ifr/{resource}"
    #
    #     # Setup Selenium WebDriver with selenium-wire
    #     options = webdriver.ChromeOptions()
    #     options.add_argument('--headless=new')
    #     options.add_argument('--disable-gpu')
    #     # options.add_argument("--start-maximized")
    #     options.add_argument("--disable-blink-features=AutomationControlled")
    #     options.add_argument("--disable-search-engine-choice-screen")
    #     download_dir = TempFolderHelper.get_temp_folder_path()
    #     options.add_experimental_option("prefs", {
    #         "download.default_directory": download_dir,
    #         "download.prompt_for_download": False,
    #         "download.directory_upgrade": True,
    #         "safebrowsing.enabled": True
    #     })
    #     # options.add_experimental_option('prefs', prefs)
    #     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    #     driver.execute_cdp_cmd('Network.setBlockedURLs', {'urls': [
    #         '*://*.googleapis.com/*',
    #         '*://*.google-analytics.com/*',
    #         '*://*.doubleclick.net/*',
    #         '*://*.googletagmanager.com/*',
    #         '*://*.google.*/*',
    #         '*://*.amplitude.com/*',
    #         # '*://*.redgifs.com/static/*.css',
    #         # '*://*.redgifs.com/static/*',
    #         '*://*.redgifs.com/assets/*',
    #         '*://*.redgifs.com/*.png',
    #         # poster
    #         '*://*.redgifs.com/*.jpg',
    #         # More specific scripts
    #         # Although it seems if any script crashes the whole page won't proceed.
    #         # '*://*.redgifs.com/static/discord_*',
    #         # '*://*.redgifs.com/static/x-*',
    #         # '*://*.redgifs.com/static/twitter-*',
    #         '*://*.redgifs.com/site.webmanifest',
    #         # '*://*.redgifs.com/static/recombee-*',
    #         # '*://*.redgifs.com/static/amplitude-*',
    #         # '*://*.redgifs.com/static/bugsnag-*',
    #         # '*://*.redgifs.com/static/ApplicationFooterContainer-*',
    #         # '*://*.redgifs.com/static/InfoBarContainer-*',
    #         # '*://*.redgifs.com/static/Popup-*',
    #         # '*://*.redgifs.com/static/EmbedPage-*',
    #         # '*://*.redgifs.com/static/Button-*',
    #         # '*://*.redgifs.com/static/ToggleButton-*',
    #         # '*://*.redgifs.com/static/plusIcon-*',
    #         # '*://*.redgifs.com/static/PlusButton-*',
    #         # '*://*.redgifs.com/static/cross-black-*',
    #         # '*://*.redgifs.com/static/BaseButton-*',
    #         # '*://*.redgifs.com/static/share-*',
    #
    #         # cdn-cgi/challenge-platform/  - this sets the cookies we need.
    #         # '*://*.redgifs.com/cdn-cgi/*',
    #     ]})
    #
    #     output = ''
    #     try:
    #         if RedgifsEmbedder.verbose_logging:
    #             print("Selenium setup, going to target url: " + target_url)
    #
    #         print(time.perf_counter() - start_time, "seconds to setup selenium")
    #         driver.get(target_url)
    #
    #         resource_casefold = resource.casefold()
    #         request = self.check_for_requests(driver, resource_casefold, 10, 0.5)
    #         if request is None:
    #             return False
    #
    #         if RedgifsEmbedder.verbose_logging:
    #             print(f"request: {request.url}")
    #
    #         cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
    #         if RedgifsEmbedder.verbose_logging:
    #             print(cookies)
    #         files_before = TempFolderHelper.get_temp_folder_files()
    #         driver.get(request.url)
    #
    #         if RedgifsEmbedder.verbose_logging:
    #             print("Waiting for download...")
    #         self.wait_for_download(download_dir, files_before, 20)
    #
    #         new_files = TempFolderHelper.get_new_temp_folder_files(files_before)
    #         # If the file ends with .m4s we want to rename it to .mp4
    #         for file in new_files:
    #             if file.endswith(".m4s"):
    #                 output = file.replace(".m4s", ".mp4")
    #                 output = os.path.join(download_dir, output)
    #                 file_path = os.path.join(download_dir, file)
    #                 if RedgifsEmbedder.verbose_logging:
    #                     print(f"Renaming '{file}' to '{output}'")
    #                 os.replace(file_path, output)
    #     finally:
    #         driver.quit()
    #
    #     end_time = time.perf_counter()
    #     print(f"Took {end_time - start_time} seconds to fetch redgifs video.")
    #     return output if output else False
    #
    # @staticmethod
    # def check_request(url, resource) -> bool:
    #     url = url.casefold()
    #     return resource in url and any(ext in url for ext in [".mp4", ".m4s"])
    #
    # @staticmethod
    # def check_for_requests(driver, resource, timeout: float = 30, interval: float = 1) -> object:
    #     start_time = time.time()
    #     seen_requests = set()
    #
    #     while time.time() - start_time < timeout:
    #         for request in driver.requests:
    #             if request.id not in seen_requests:
    #                 seen_requests.add(request.id)
    #                 if RedgifsEmbedder.verbose_logging:
    #                     print(f"Checking request {request.url}")
    #                 if RedgifsEmbedder.check_request(request.url, resource):
    #                     return request
    #         time.sleep(interval)
    #
    #     return None
    #
    # @staticmethod
    # def wait_for_download(download_path, files_before, timeout=30):
    #     time.sleep(0.1)
    #     seconds = 0
    #
    #     while RedgifsEmbedder.check_if_any_pending_downloads(download_path, files_before):
    #         time.sleep(1)
    #         if RedgifsEmbedder.verbose_logging:
    #             print(f"Waiting for download... {seconds}")
    #         seconds += 1
    #         if seconds > timeout:
    #             return False
    #
    #     return True
    #
    # @staticmethod
    # def check_if_any_pending_downloads(download_path, files_before):
    #     files = os.listdir(download_path)
    #     if len(files) == len(files_before):
    #         print(f"Same amount of files found: {len(files)}")
    #         return True
    #
    #     for file in files:
    #         if file.endswith('.crdownload'):
    #             return True
    #
    #     if RedgifsEmbedder.verbose_logging:
    #         print(f"No pending downloads after {len(files)} before {len(files_before)}")
    #     return False
    #
    @staticmethod
    def get_resource(url):
        match = redgifs_url_regex.match(url)
        if match:
            return match.group('resource')

        return None