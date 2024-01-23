import logging
import time
from datetime import datetime
from typing import Union

from PIL import Image

from .displays import Display
from .asset import Asset
from .chart_renderer import ChartRenderer


class Monitor:
    def __init__(
        self,
        display: Display,
        assets: list[Asset],
        charts: list[ChartRenderer],
        refresh_delay: int = 180,
        screen_safe_interval: Union[int, None] = None,
    ):
        self.display = display
        self.assets = assets
        self.charts = charts
        self.refresh_delay = refresh_delay
        self.screen_safe_interval = screen_safe_interval
        self.last_full_refresh = datetime.now()

    def _update_display(self):
        screen_split_interval = self.display.height // len(self.assets)
        self.display.wake_up()
        image = Image.new("1", (self.display.width, self.display.height), 255)
        for i, chart in enumerate(self.charts):
            image.paste(chart.get_image(), (0, i * (screen_split_interval)))
        if (
            self.screen_safe_interval
            and (datetime.now() - self.last_full_refresh).seconds
            > self.screen_safe_interval
        ):
            logging.debug("Refreshing screen via screen safe refresh...")
            self.last_full_refresh = datetime.now()
            self.display.update(image)
        else:
            logging.debug("Refreshing screen via fast refresh...")
            self.display.fast_update(image)
        self.display.sleep()

    def start(self) -> None:
        prev_change = [float("inf")] * len(self.assets)
        logging.info("Monitoring asset...")
        self.display.init()
        while True:
            logging.debug("Refreshing asset(s)...")
            curr_change = []
            for asset in self.assets:
                asset.refresh()
                curr_change.append("{:.2f}".format(asset.change))
            if curr_change != prev_change:
                logging.info("Asset change detected")
                self._update_display()
            prev_change = curr_change
            time.sleep(self.refresh_delay)

    def stop(self):
        logging.info("Stopping monitor...")
        self.display.clear()
        self.display.sleep()
