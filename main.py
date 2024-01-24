import argparse
import logging

import yaml

from asset_monitor import Monitor, ChartRenderer, Asset, DisplayFactory
from asset_monitor.displays import Display


class ConfigError(Exception):
    pass


def get_config() -> any:
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("--dev", action="store_true")
    args = parser.parse_args()
    with open("config.yml") as f:
        config = yaml.safe_load(f)
    config["dev"] = args.dev
    return config


def get_display(config: any) -> Display:
    logging.info("Initialising display...")
    if config["dev"]:
        logging.root.setLevel(level=logging.DEBUG)
        return DisplayFactory.get("dev")
    else:
        return DisplayFactory.get(config["display"]["id"])


def get_assets(config: any) -> list[Asset]:
    logging.info("Initialising assets...")
    assets = []
    if not config.get("assets"):
        raise ConfigError("No assets provided in config.")
    for asset in config["assets"]:
        assets.append(Asset(asset["ticker"], asset.get("name")))
    return assets


def get_charts(assets: list[Asset], config: any) -> list[ChartRenderer]:
    logging.info("Initialising renderers...")
    screen_split_interval = display.height // len(assets)
    charts = []
    for asset in assets:
        charts.append(
            ChartRenderer(
                display.width,
                screen_split_interval,
                asset,
                candles=config.get("chart", {}).get("candles"),
                flipped=config.get("display", {}).get("flipped"),
                font=config.get("chart", {}).get("font"),
                font_variant=config.get("chart", {}).get("font_variant"),
                font_size=config.get("chart", {}).get("font_size"),
            )
        )
    return charts


if __name__ == "__main__":
    logging.basicConfig()
    config = get_config()
    display = get_display(config)
    assets = get_assets(config)
    charts = get_charts(assets, config)
    asset_monitor = Monitor(
        display,
        assets,
        charts,
        refresh_delay=config.get("refresh_delay", 180),
        screen_safe_interval=config.get("screen_safe_interval"),
    )
    try:
        asset_monitor.start()
    except KeyboardInterrupt:
        asset_monitor.stop()
