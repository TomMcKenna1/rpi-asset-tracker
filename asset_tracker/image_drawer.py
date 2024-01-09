from PIL import Image, ImageDraw, ImageFont

from .asset import Asset


class ImageDrawer:
    """
    Class to construct an image
    """

    def __init__(self, width: int, height: int, asset: Asset, font: str = "Roboto.ttf", font_size: int = 30):
        self.width = width
        self.height = height
        self.asset_name = asset.name
        self.asset_last_close = str(round(asset.price, 2))
        self.asset_change = str(round(asset.change, 2))+"%"
        self.font30 = ImageFont.truetype(font, size=font_size)
        self.font30.set_variation_by_name("ExtraBold")
        ascent, descent = self.font30.getmetrics()
        self.meta_font_height = ascent + descent
        self.bar_thickness = 1
        self.meta_start_height = self.height - self.meta_font_height

    def _draw_meta_divider(self, draw):
        metadata_divider = [
            (0, self.meta_start_height - self.bar_thickness),
            (self.width, self.meta_start_height),
        ]
        draw.rectangle(metadata_divider, fill=0)

    def _draw_meta_name(self, draw):
        name_text_length = self.font30.getlength(self.asset_name)
        name_divider = [
            (20 + name_text_length, self.meta_start_height + self.meta_font_height // 5),
            (20 + name_text_length + self.bar_thickness, self.height - self.meta_font_height // 5),
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
            (self.width - change_text_length - 20, self.meta_start_height + self.meta_font_height // 5),
            (self.width - change_text_length - 20 + self.bar_thickness, self.height - self.meta_font_height // 5),
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
