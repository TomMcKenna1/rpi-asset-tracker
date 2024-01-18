from abc import ABC, abstractmethod

from PIL import Image


class Display(ABC):
    """
    The base class for a display implementation.
    """

    @property
    @abstractmethod
    def width(self) -> int:
        pass

    @property
    @abstractmethod
    def height(self) -> int:
        pass

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def update(self, image: Image.Image):
        pass

    @abstractmethod
    def fast_update(self, image: Image.Image):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def enter_standby(self):
        pass
