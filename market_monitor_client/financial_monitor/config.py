import logging
from typing import Any

import yaml

from .displays import DisplayFactory, Display
from .asset import Asset
from .chart_renderer import ChartRenderer


DEFAULT_REFRESH_DELAY = 180  # 3 minutes
DEFAULT_SCREEN_SAFE_INTERVAL = 86400  # 24 hours
DEFAULT_LINE_WIDTH = 2

class Config:
    def __init__(
        self,
        uuid,
        asset_list,
        display_type,
        flipped=False,
        candles=False,
        line_width=DEFAULT_LINE_WIDTH,
        font=None,
        font_variant=None,
        font_size=None,
        refresh_delay=DEFAULT_REFRESH_DELAY,
        screen_safe_interval=DEFAULT_SCREEN_SAFE_INTERVAL,
    ):
        self._uuid = uuid
        self._display = DisplayFactory.get(display_type)
        self._assets = []
        self._charts = []
        self._flipped = flipped
        self._candles = candles
        self._line_width = line_width
        self._font = font
        self._font_variant = font_variant
        self._font_size = font_size
        self._refresh_delay = refresh_delay
        self._screen_safe_interval = screen_safe_interval
        self.assets = asset_list

    @classmethod
    def from_yaml(cls, path, **kwargs) -> Any:
        with open(path) as f:
            config = yaml.safe_load(f)
        if kwargs.get("dev"):
            config["display"]["id"] = "dev"
        return cls(
            config["uuid"],
            config["assets"],
            config["display"]["id"],
            config["display"].get("flipped"),
            config["display"].get("candles"),
            config.get("line_width", DEFAULT_LINE_WIDTH),
            config.get("font"),
            config.get("font_variant"),
            config.get("font_size"),
            config.get("refresh_delay", DEFAULT_REFRESH_DELAY),
            config.get("screen_safe_interval", DEFAULT_SCREEN_SAFE_INTERVAL),
        )

    @property
    def display(self) -> Display:
        return self._display
    
    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def assets(self) -> list[Asset]:
        return self._assets

    @assets.setter
    def assets(self, asset_list: list[dict[str, str]]):
        logging.info("Initialising assets...")
        assets = []
        charts = []
        screen_split_interval = self._display.height // len(asset_list)
        for asset in asset_list:
            asset_instance = Asset(asset["ticker"], asset.get("name"))
            assets.append(asset_instance)
            charts.append(
                ChartRenderer(
                    self._display.width,
                    screen_split_interval,
                    asset_instance,
                    candles=self._candles,
                    line_width=self._line_width,
                    font=self._font,
                    font_variant=self._font_variant,
                    font_size=self._font_size,
                )
            )
        self._assets = assets
        self._charts = charts

    @property
    def charts(self) -> list[ChartRenderer]:
        return self._charts

    @property
    def flipped(self) -> bool:
        return self._flipped

    @flipped.setter
    def flipped(self, value: bool):
        if isinstance(value, bool):
            self._flipped = value
        else:
            raise TypeError("Config item 'flipped' must be of type bool")

    @property
    def candles(self) -> bool:
        return self._candles

    @candles.setter
    def candles(self, value: bool):
        if isinstance(value, bool):
            self._candles = value
        else:
            raise TypeError("Config item 'candles' must be of type bool")

    @property
    def line_width(self) -> int:
        return self._line_width

    @line_width.setter
    def line_width(self, value: int):
        if isinstance(value, int):
            self._line_width = value
        else:
            raise TypeError("Config item 'line_width' must be of type int")
        
    @property
    def font(self) -> str:
        return self._font

    @font.setter
    def font(self, value: str):
        if isinstance(value, str):
            self._font = value
        else:
            raise TypeError("Config item 'font' must be of type str")

    @property
    def font_variant(self) -> str:
        return self._font_variant

    @font_variant.setter
    def font_variant(self, value: str):
        if isinstance(value, str):
            self._font_variant = value
        else:
            raise TypeError("Config item 'font_variant' must be of type str")

    @property
    def font_size(self) -> int:
        return self._font_size

    @font_size.setter
    def font_size(self, value: int):
        if isinstance(value, int):
            self._font_size = value
        else:
            raise TypeError("Config item 'font_size' must be of type int")

    @property
    def refresh_delay(self) -> int:
        return self._refresh_delay

    @refresh_delay.setter
    def refresh_delay(self, value: int):
        if isinstance(value, int):
            self._refresh_delay = value
        else:
            raise TypeError("Config item 'refresh_delay' must be of type int")

    @property
    def screen_safe_interval(self) -> int:
        return self._screen_safe_interval

    @screen_safe_interval.setter
    def screen_safe_interval(self, value: int):
        if isinstance(value, int):
            self._screen_safe_interval = value
        else:
            raise TypeError("Config item 'screen_safe_interval' must be of type int")
