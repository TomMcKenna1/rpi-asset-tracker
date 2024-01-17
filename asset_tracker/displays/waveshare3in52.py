import logging

try:
    from waveshare_epd import epd3in52
except ImportError:
    pass

from .base import Display
from .display_factory import DisplayFactory


@DisplayFactory.register("waveshare_3in52")
class Waveshare3in52(Display):
    """
    Display class supporting a waveshare 3"52 e-ink display
    """

    def __init__(self):
        self.epd = epd3in52.EPD()

    @property
    def width(self) -> int:
        return epd.width

    @property
    def height(self) -> int:
        return epd.height

    def init(self):
        self.epd.init()
        self.epd.display_NUM(self.epd.WHITE)
        self.epd.lut_GC()
        self.epd.refresh()
        self.epd.send_command(0x50)
        self.epd.send_data(0x17)

    def update(self, image):
        self.epd.display(self.epd.getbuffer(image))
        self.epd.lut_GC()
        self.epd.refresh()

    def enter_standby(self):
        self.epd.sleep()
