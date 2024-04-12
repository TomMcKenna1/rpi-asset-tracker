from typing import Union

from PIL import Image, ImageDraw, ImageFont

from .asset import Asset


class ChartRenderer:
    """
    Class to render chart images of an asset.
    """

    def __init__(
        self,
        width: int,
        height: int,
        asset: Asset,
        candles: bool = False,
        line_width: int = 0,
        font: Union[str, None] = None,
        font_variant: Union[str, None] = None,
        font_size: Union[int, None] = None,
    ):
        self.width = width
        self.height = height
        self.asset = asset
        self.candles = candles
        self.line_width = line_width
        if font:
            self.font = ImageFont.truetype(font, size=font_size)
        else:
            self.font = ImageFont.load_default(size=font_size)
        if font_variant:
            self.font.set_variation_by_name(font_variant)
        font_top, font_bottom = self.font.getmetrics()
        self.meta_font_height = font_top + font_bottom
        self.bar_thickness = 1
        self.meta_start_height = self.height - self.meta_font_height

    @property
    def pixel_factor(self) -> float:
        return self.meta_start_height / (
            self.asset.history["High"].max() - self.asset.history["Low"].min()
        )

    def draw_text_with_outline(self, draw, text, position, font, outline_thickness):
        for i in range(1, outline_thickness + 1):
            outline_position = (position[0] - i, position[1])
            draw.text(outline_position, text, font=font, fill=0)
            outline_position = (position[0] + i, position[1])
            draw.text(outline_position, text, font=font, fill=0)
            outline_position = (position[0], position[1] - i)
            draw.text(outline_position, text, font=font, fill=0)
            outline_position = (position[0], position[1] + i)
            draw.text(outline_position, text, font=font, fill=0)
        draw.text(position, text, font=font, fill=1)

    def _draw_metadata_divider(self, draw: ImageDraw.ImageDraw) -> None:
        metadata_divider = [
            (0, self.meta_start_height - self.bar_thickness),
            (self.width, self.meta_start_height),
        ]
        draw.rectangle(metadata_divider, fill=0)

    def _draw_metadata_name(self, draw: ImageDraw.ImageDraw) -> None:
        name_text_length = self.font.getlength(self.asset.name)
        name_divider = [
            (
                20 + name_text_length,
                self.meta_start_height + self.meta_font_height // 5,
            ),
            (
                20 + name_text_length + self.bar_thickness,
                self.height - self.meta_font_height // 5,
            ),
        ]
        draw.text(
            (10, self.meta_start_height),
            self.asset.name,
            font=self.font,
            fill=0,
        )
        draw.rectangle(name_divider, fill=0)

    def _draw_metadata_price(self, draw: ImageDraw.ImageDraw) -> None:
        asset_last_close = "{:.2f}".format(self.asset.price)
        last_close_text_length = self.font.getlength(asset_last_close)
        draw.text(
            (self.width // 2 - last_close_text_length // 2, self.meta_start_height),
            asset_last_close,
            font=self.font,
            fill=0,
        )

    def _draw_metadata_change(self, draw: ImageDraw.ImageDraw) -> None:
        asset_change_num = "{:.2f}".format(self.asset.change)
        suffix = "%"
        is_positive = self.asset.change >= 0
        change_text_length = self.font.getlength(asset_change_num)
        suffix_text_length = self.font.getlength(suffix)
        change_divider = [
            (
                self.width - change_text_length - suffix_text_length - 20,
                self.meta_start_height + self.meta_font_height // 5,
            ),
            (
                self.width
                - change_text_length
                - suffix_text_length
                - 20
                + self.bar_thickness,
                self.height - self.meta_font_height // 5,
            ),
        ]
        if is_positive:
            print('positive')
            self.draw_text_with_outline(
                draw,
                asset_change_num,
                (
                    self.width - change_text_length - suffix_text_length - 10,
                    self.meta_start_height,
                ),
                self.font,
                2,
            )
        else:
            print('negative')
            draw.text(
                (
                    self.width - change_text_length - suffix_text_length - 10,
                    self.meta_start_height,
                ),
                asset_change_num,
                font=self.font,
                fill=0,
            )
        draw.text(
            (
                self.width - suffix_text_length - 10,
                self.meta_start_height,
            ),
            suffix,
            font=self.font,
            fill=0,
        )
        draw.rectangle(change_divider, fill=0)

    def _draw_asset_metadata(self, draw: ImageDraw.ImageDraw) -> None:
        self._draw_metadata_divider(draw)
        self._draw_metadata_name(draw)
        self._draw_metadata_price(draw)
        self._draw_metadata_change(draw)

    def _draw_candle(
        self,
        draw: ImageDraw.ImageDraw,
        start: int,
        asset_low: float,
        open: float,
        high: float,
        low: float,
        close: float,
    ) -> None:
        candle_width = 4 * ((self.width - 20) / len(self.asset.history.index)) // 10
        if open < close:
            open_close_top = close
            open_close_bottom = open
            fill = 1
        else:
            open_close_top = open
            open_close_bottom = close
            fill = 0
        high_low_line = [
            (
                start,
                self.meta_start_height - ((high - asset_low) * self.pixel_factor),
            ),
            (
                start,
                self.meta_start_height - ((low - asset_low) * self.pixel_factor),
            ),
        ]
        open_close_bar = [
            (
                start - candle_width,
                self.meta_start_height
                - ((open_close_top - asset_low) * self.pixel_factor),
            ),
            (
                start + candle_width,
                self.meta_start_height
                - ((open_close_bottom - asset_low) * self.pixel_factor),
            ),
        ]
        draw.line(high_low_line)
        draw.rectangle(open_close_bar, fill=fill, outline=0)

    def _draw_history(self, draw: ImageDraw.ImageDraw, candles: bool = False) -> None:
        asset_low = self.asset.history["Low"].min()
        start = 10
        increment = (self.width - 10) / len(self.asset.history.index)
        if candles:
            for x, (open, high, low, close) in enumerate(
                zip(
                    self.asset.history["Open"],
                    self.asset.history["High"],
                    self.asset.history["Low"],
                    self.asset.history["Close"],
                )
            ):
                self._draw_candle(
                    draw, start + (increment * x), asset_low, open, high, low, close
                )
        else:
            draw.line(
                [
                    (
                        start + (increment * x),
                        self.meta_start_height - ((y - asset_low) * self.pixel_factor),
                    )
                    for x, y in enumerate(self.asset.history["Close"])
                ],
                width=self.line_width,
            )

    def _draw_message(self, draw: ImageDraw.ImageDraw, message: str) -> None:
        draw.text(
            (0, 0),
            message,
            font=self.font,
            fill=0,
        )

    def get_image(self) -> Image.Image:
        image = Image.new("1", (self.width, self.height), 255)
        draw = ImageDraw.Draw(image)
        if self.asset.error_message:
            self._draw_message(draw)
        else:
            self._draw_asset_metadata(draw)
            self._draw_history(draw, candles=self.candles)
        return image
