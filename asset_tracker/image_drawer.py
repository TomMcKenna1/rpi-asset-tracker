from PIL import Image, ImageDraw, ImageFont

from .asset import Asset


class ImageDrawer:
    """
    Class to construct an image
    """

    def __init__(self, width: int, height: int, asset: Asset, font: str = "Roboto.ttf"):
        self.width = width
        self.height = height
        self.asset_name = asset.name
        self.asset_last_close = str(round(asset.price, 2))
        self.font30 = ImageFont.truetype(font, size=30)
        self.font30.set_variation_by_name("ExtraBold")

    def draw_asset_metadata(self, draw, bar_thickness: int = 1):
        ascent, descent = self.font30.getmetrics()
        text_height = ascent + descent
        meta_start_height = self.height - text_height
        name_text_length = self.font30.getlength(self.asset_name)
        last_close_text_length = self.font30.getlength(self.asset_last_close)
        percent_change_text_length = self.font30.getlength(self.asset_last_close)
        metadata_divider = [
            (0, meta_start_height - bar_thickness),
            (self.width, meta_start_height),
        ]
        name_divider = [
            (20 + name_text_length, meta_start_height + text_height // 5),
            (20 + name_text_length + bar_thickness, self.height - text_height // 5),
        ]
        draw.text(
            (10, meta_start_height),
            self.asset_name,
            font=self.font30,
            fill=0,
        )
        draw.text(
            (self.width // 2 - last_close_text_length // 2, meta_start_height),
            self.asset_last_close,
            font=self.font30,
            fill=0,
        )
        draw.rectangle(metadata_divider, fill=0)
        draw.rectangle(name_divider, fill=0)

    def get_image(self, flipped=False) -> Image:
        image = Image.new("1", (self.width, self.height), 255)
        draw = ImageDraw.Draw(image)
        self.draw_asset_metadata(draw)
        if flipped:
            return image.transpose(Image.FLIP_TOP_BOTTOM).transpose(
                Image.FLIP_LEFT_RIGHT
            )
        else:
            return image
