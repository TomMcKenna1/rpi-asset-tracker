import argparse
import logging
import time

import yaml
from PIL import Image

from asset_tracker import ChartRenderer, Asset, DisplayFactory


def get_config() -> any:
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("--dev", action="store_true")
    args = parser.parse_args()
    with open("config.yml") as f:
        config = yaml.safe_load(f)
    config["dev"] = args.dev
    return config


def start_monitoring(display, config):
    logging.info("Initialising asset(s)...")
    assets = []
    for asset in config["assets"]:
        assets.append(Asset(asset["ticker"], asset.get("name")))
    logging.info("Initialising renderers...")
    renderers = []
    for asset in assets:
        renderers.append(
            ChartRenderer(
                display.width,
                display.height // len(assets),
                asset,
                candles=config["candles"],
                flipped=config["display"]["flipped"],
            )
        )
    prev_change = [float("inf")] * len(assets)
    logging.info("Monitoring asset...")
    while True:
        logging.debug("Refreshing asset(s)...")
        curr_change = []
        for asset in assets:
            asset.refresh()
            curr_change.append("{:.2f}".format(asset.change))
        if curr_change != prev_change:
            logging.info("Asset change detected")
            display.init()
            main_image = Image.new("1", (display.width, display.height), 255)
            for i, renderer in enumerate(renderers):
                main_image.paste(
                    renderer.get_image(), (0, i * (display.height // len(assets)))
                )
            display.update(main_image)
            display.enter_standby()
        prev_change = curr_change
        time.sleep(config["refresh_delay"])


if __name__ == "__main__":
    try:
        logging.basicConfig()
        config = get_config()
        logging.info("Initialising display...")
        if config["dev"]:
            logging.root.setLevel(level=logging.DEBUG)
            display = DisplayFactory.get("dev")
        else:
            display = DisplayFactory.get(config["display"]["name"])
        start_monitoring(display, config)
    except KeyboardInterrupt:
        logging.info("Clearing and sleeping display...")
        display.clear()
        display.enter_standby()
        logging.info("Exited successfully")
