import logging
import time

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
    ):
        self.display = display
        self.assets = assets
        self.charts = charts
        self.refresh_delay = refresh_delay

    def start(self) -> None:
        screen_split_interval = self.display.height // len(self.assets)
        prev_change = [float("inf")] * len(self.assets)
        logging.info("Monitoring asset...")
        while True:
            logging.debug("Refreshing asset(s)...")
            curr_change = []
            for asset in self.assets:
                asset.refresh()
                curr_change.append("{:.2f}".format(asset.change))
            if curr_change != prev_change:
                logging.info("Asset change detected")
                self.display.init()
                main_image = Image.new(
                    "1", (self.display.width, self.display.height), 255
                )
                for i, chart in enumerate(self.charts):
                    main_image.paste(
                        chart.get_image(), (0, i * (screen_split_interval))
                    )
                self.display.fast_update(main_image)
                self.display.enter_standby()
            prev_change = curr_change
            time.sleep(self.refresh_delay)

    def stop(self):
        logging.info("Clearing and sleeping display...")
        self.display.clear()
        self.display.enter_standby()
        logging.info("Monitor stopped successfully")
