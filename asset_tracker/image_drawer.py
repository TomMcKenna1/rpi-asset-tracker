from PIL import Image, ImageDraw, ImageFont

from .asset import Asset


class ImageDrawer:
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
        self.font30 = ImageFont.truetype(font, size=font_size)
        self.font30.set_variation_by_name("ExtraBold")
        ascent, descent = self.font30.getmetrics()
        self.meta_font_height = ascent + descent
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
        name_text_length = self.font30.getlength(self.asset_name)
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
            font=self.font30,
            fill=0,
        )
        draw.rectangle(name_divider, fill=0)

    def _draw_meta_price(self, draw):
        last_close_text_length = self.font30.getlength(self.asset_last_close)
        draw.text(
            (self.width // 2 - last_close_text_length // 2, self.meta_start_height),
            self.asset_last_close,
            font=self.font30,
            fill=0,
        )

    def _draw_meta_change(self, draw):
        change_text_length = self.font30.getlength(self.asset_change)
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
            font=self.font30,
            fill=0,
        )
        draw.rectangle(change_divider, fill=0)

    def draw_asset_metadata(self, draw):
        self._draw_meta_divider(draw)
        self._draw_meta_name(draw)
        self._draw_meta_price(draw)
        self._draw_meta_change(draw)

    def draw_candle(self, draw, start, open, high, low, close):
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
                start - 1,
                self.meta_start_height
                - ((high - self.asset_history["Low"].min()) * self.pixel_factor),
            ),
            (
                start,
                self.meta_start_height
                - ((low - self.asset_history["Low"].min()) * self.pixel_factor),
            ),
        ]
        open_close_bar = [
            (
                start - 3,
                self.meta_start_height
                - ((open_close_top - self.asset_history["Low"].min()) * self.pixel_factor),
            ),
            (
                start + 2,
                self.meta_start_height
                - ((open_close_bottom - self.asset_history["Low"].min()) * self.pixel_factor),
            ),
        ]
        draw.rectangle(high_low_line, fill=0)
        draw.rectangle(open_close_bar, fill=fill, outline=0)

    def draw_history(self, draw, candles=False):
        start = 10
        increment = (self.width)/len(self.asset_history.index)
        for open, high, low, close in zip(
            self.asset_history["Open"],
            self.asset_history["High"],
            self.asset_history["Low"],
            self.asset_history["Close"],
        ):
            self.draw_candle(draw, start, open, high, low, close)
            start += int(increment)

    def get_image(self, flipped=False) -> Image:
        image = Image.new("1", (self.width, self.height), 255)
        draw = ImageDraw.Draw(image)
        self.draw_asset_metadata(draw)
        self.draw_history(draw, candles=True)
        if flipped:
            return image.transpose(Image.FLIP_TOP_BOTTOM).transpose(
                Image.FLIP_LEFT_RIGHT
            )
        else:
            return image
