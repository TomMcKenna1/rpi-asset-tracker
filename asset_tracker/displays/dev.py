from .base import Display
from .display_factory import DisplayFactory


@DisplayFactory.register("dev")
class Dev(Display):
    """
    Display class to be used only for development purposes
    """

    def __init__(self, width: int = 360, height: int = 240):
        self._width = width
        self._height = height

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @width.setter
    def width(self, value) -> None:
        self._width = value

    @height.setter
    def height(self, value) -> None:
        self._height = value

    def init(self):
        pass

    def update(self, image):
        image.show()

    def clear(self):
        pass

    def enter_standby(self):
        pass
