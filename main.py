import argparse
import logging
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
    logging.info("Gathering latest data...")
    asset = Asset(config["ticker_symbol"])
    logging.info("Data gathered.")
    logging.info("Drawing image...")
    chart_drawer = ChartDrawer(display.get_width(), display.get_height(), asset, flipped=config["display"]["flipped"])
    latest_image = chart_drawer.get_image(candles=config["chart"]["candles"])
    logging.info("Image completed.")
    logging.info("Sending to display...")
    # latest_image.show()
    display.update(latest_image)
    logging.info("Finished, sleeping the display.")
    display.enter_standby()


if __name__ == "__main__":
    config = get_config()
    if config["dev"]:
        logging.basicConfig(level=logging.DEBUG)
        display = DisplayFactory.get("dev")
    else:
        display = DisplayFactory.get(config["display"]["name"])
    start_monitoring(display, config)
