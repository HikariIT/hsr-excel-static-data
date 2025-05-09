import requests
import logging
import random
import time


class HoneyHunterImporter:

    URL_BASE = 'https://starrail.honeyhunterworld.com/'
    SUB_URL_ITEM = 'img/item/'

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        })

    def download_light_cone_image(self, light_cone_name: str, light_cone_id: int) -> None:
        name = ''.join([char.lower() for char in light_cone_name if char.isalnum() or char in [' ']])
        name = '-'.join(name.split(' '))
        save_dir = 'output/img/light-cone-icon/'
        icon_url = f"{self.URL_BASE}{self.SUB_URL_ITEM}{name}-item_icon.webp"

        self._random_sleep()
        self.logger.debug(f"Downloading light cone image from {icon_url}")

        response = self.session.get(icon_url, stream=True)
        if response.status_code == 200:
            with open(f"{save_dir}{light_cone_id}.webp", 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            self.logger.info(f"Downloaded light cone image: {name}.webp")
        else:
            self.logger.error(f"Failed to download light cone image: {icon_url} (Status code: {response.status_code})")

    def _random_sleep(self, min_seconds: float = 0.5, max_seconds: float = 3.0) -> None:
        sleep_time = random.uniform(min_seconds, max_seconds)
        self.logger.debug(f"Sleeping for {sleep_time:.2f} seconds")
        time.sleep(sleep_time)