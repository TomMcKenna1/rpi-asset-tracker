from PIL import Image, ImageDraw, ImageFont

from .asset import Asset


class ChartDrawer:
    def __init__(
        self,
        width: int,
        height: int,
        asset: Asset,
        font: str = "Roboto.ttf",
        font_size: int = 30,
    ):
        self.width = width
        self.height = height
        self.asset_name = asset.name
        self.asset_last_close = str(round(asset.price, 2))
        self.asset_change = str(round(asset.change, 2)) + "%"
        self.asset_history = asset.history
        self.font = ImageFont.truetype(font, size=font_size)
        self.font.set_variation_by_name("ExtraBold")
        font_top, font_bottom = self.font.getmetrics()
        self.meta_font_height = font_top + font_bottom
        self.bar_thickness = 1
        self.meta_start_height = self.height - self.meta_font_height
        self.asset_low = self.asset_history["Low"].min()
        self.asset_high = self.asset_history["High"].max()
        self.pixel_factor = self.meta_start_height / (self.asset_high - self.asset_low)

    def _draw_meta_divider(self, draw):
        metadata_divider = [
            (0, self.meta_start_height - self.bar_thickness),
            (self.width, self.meta_start_height),
        ]
        draw.rectangle(metadata_divider, fill=0)

    def _draw_meta_name(self, draw):
        name_text_length = self.font.getlength(self.asset_name)
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
            self.asset_name,
            font=self.font,
            fill=0,
        )
        draw.rectangle(name_divider, fill=0)

    def _draw_meta_price(self, draw):
        last_close_text_length = self.font.getlength(self.asset_last_close)
        draw.text(
            (self.width // 2 - last_close_text_length // 2, self.meta_start_height),
            self.asset_last_close,
            font=self.font,
            fill=0,
        )

    def _draw_meta_change(self, draw):
        change_text_length = self.font.getlength(self.asset_change)
        change_divider = [
            (
                self.width - change_text_length - 20,
                self.meta_start_height + self.meta_font_height // 5,
            ),
            (
                self.width - change_text_length - 20 + self.bar_thickness,
                self.height - self.meta_font_height // 5,
            ),
        ]

        draw.text(
            (self.width - change_text_length - 10, self.meta_start_height),
            self.asset_change,
            font=self.font,
            fill=0,
        )
        draw.rectangle(change_divider, fill=0)

    def _draw_asset_metadata(self, draw):
        self._draw_meta_divider(draw)
        self._draw_meta_name(draw)
        self._draw_meta_price(draw)
        self._draw_meta_change(draw)

    def _draw_candle(self, draw, start, open, high, low, close):
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
                self.meta_start_height - ((high - self.asset_low) * self.pixel_factor),
            ),
            (
                start,
                self.meta_start_height - ((low - self.asset_low) * self.pixel_factor),
            ),
        ]
        open_close_bar = [
            (
                start - 2,
                self.meta_start_height
                - ((open_close_top - self.asset_low) * self.pixel_factor),
            ),
            (
                start + 2,
                self.meta_start_height
                - ((open_close_bottom - self.asset_low) * self.pixel_factor),
            ),
        ]
        draw.line(high_low_line)
        draw.rectangle(open_close_bar, fill=fill, outline=0)

    def _draw_history(self, draw, candles=False):
        start = 10
        increment = (self.width - 10) / len(self.asset_history.index)
        if candles:
            for x, (open, high, low, close) in enumerate(
                zip(
                    self.asset_history["Open"],
                    self.asset_history["High"],
                    self.asset_history["Low"],
                    self.asset_history["Close"],
                )
            ):
                self._draw_candle(draw, start + (increment * x), open, high, low, close)
        else:
            draw.line(
                [
                    (
                        start + (increment * x),
                        self.meta_start_height
                        - ((y - self.asset_low) * self.pixel_factor),
                    )
                    for x, y in enumerate(self.asset_history["Close"])
                ]
            )

    def get_image(self, flipped=False) -> Image.Image:
        image = Image.new("1", (self.width, self.height), 255)
        draw = ImageDraw.Draw(image)
        self._draw_asset_metadata(draw)
        self._draw_history(draw, candles=True)
        if flipped:
            return image.transpose(Image.FLIP_TOP_BOTTOM).transpose(
                Image.FLIP_LEFT_RIGHT
            )
        else:
            return image
