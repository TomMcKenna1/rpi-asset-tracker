import logging
import asyncio
from datetime import datetime
from collections import deque

from PIL import Image

from .config import Config

LOOP_INTERVAL = 0.1


class Monitor:
    def __init__(
        self,
        config: Config,
    ):
        self.config = config
        self.last_full_refresh = datetime.now()
        self.running = False
        self.updating = False
        self._pause = False
        self._pause_q = deque()

    @property
    def pause(self):
        if self._pause_q:
            self._pause = self._pause_q[0]
            return self._pause_q.popleft()
        return self._pause

    @pause.setter
    def pause(self, value):
        if self._pause_q:
            to_check = self._pause_q[-1]
        else:
            to_check = self._pause
        if to_check != value:
            self._pause_q.append(value)

    def _update_display(self):
        screen_split_interval = self.config.display.height // len(self.config.assets)
        self.config.display.wake_up()
        image = Image.new(
            "1", (self.config.display.width, self.config.display.height), 255
        )
        for i, chart in enumerate(self.config.charts):
            image.paste(chart.get_image(), (0, i * (screen_split_interval)))
        if self.config.flipped:
            image = image.transpose(Image.FLIP_TOP_BOTTOM).transpose(
                Image.FLIP_LEFT_RIGHT
            )
        if (
            self.config.screen_safe_interval
            and (datetime.now() - self.last_full_refresh).seconds
            > self.config.screen_safe_interval
        ):
            logging.debug("Refreshing screen via screen safe refresh...")
            self.last_full_refresh = datetime.now()
            self.config.display.update(image)
        else:
            logging.debug("Refreshing screen via fast refresh...")
            self.config.display.fast_update(image)
        self.config.display.sleep()

    async def start(self) -> None:
        self.running = True
        prev_change = [float("inf")] * len(self.config.assets)
        logging.info("Monitoring asset...")
        self.config.display.init()
        while self.running:
            self.updating = True
            logging.debug("Refreshing asset(s)...")
            curr_change = []
            for asset in self.config.assets:
                asset.refresh()
                curr_change.append("{:.2f}".format(asset.change))
            if curr_change != prev_change:
                logging.info("Asset change detected")
                self._update_display()
            prev_change = curr_change
            self.updating = False
            last_refresh = datetime.now()
            while (datetime.now() - last_refresh).seconds < self.config.refresh_delay:
                if not self.running or self.pause:
                    while self.pause and self.running:
                        await asyncio.sleep(LOOP_INTERVAL)
                    break
                await asyncio.sleep(LOOP_INTERVAL)

    async def stop(self):
        logging.info("Stopping monitor...")
        while self.updating:
            await asyncio.sleep(LOOP_INTERVAL)
        self.pause = False
        self.running = False
        self.config.display.wake_up()
        self.config.display.clear()
        self.config.display.sleep()
