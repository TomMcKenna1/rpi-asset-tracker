import argparse
import logging
import time

import yaml

from asset_tracker import ChartDrawer, Asset, DisplayFactory


def get_config() -> any:
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument(
        "ticker_symbol", help="The ticker symbol of the asset being tracked.", type=str
    )
    parser.add_argument("--dev", action="store_true")
    args = parser.parse_args()
    with open("config.yml") as f:
        config = yaml.safe_load(f)
    config["dev"] = args.dev
    config["ticker_symbol"] = args.ticker_symbol
    return config


def start_monitoring(display, config):
    logging.info("Initialising asset...")
    asset = Asset(config["ticker_symbol"])
    logging.info("Initialising renderer...")
    chart_drawer = ChartDrawer(
        display.width, display.height, asset, flipped=config["display"]["flipped"]
    )
    prev_change = -1
    logging.info("Monitoring asset...")
    while True:
        logging.debug("Refreshing asset...")
        asset.refresh()
        curr_change = "{:.2f}".format(asset.change)
        if curr_change != prev_change:
            logging.info("Asset change detected")
            display.init()
            latest_image = chart_drawer.get_image(candles=config["chart"]["candles"])
            display.update(latest_image)
            display.enter_standby()
        prev_change = curr_change
        time.sleep(config["refresh_rate"])


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
        logging.info("Sleeping display...")
        display.enter_standby()
        logging.info("Exited successfully")
