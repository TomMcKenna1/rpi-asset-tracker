from .base import Display
from .display_factory import DisplayFactory


@DisplayFactory.register("dev")
class Dev(Display):
    def __init__(self, width: int = 360, height: int = 240):
        self.width = width
        self.height = height

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def update(self, image):
        image.show()

    def enter_standby(self):
        pass
