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
    def init(self) -> None:
        pass

    @abstractmethod
    def update(self, image: Image.Image) -> None:
        pass

    @abstractmethod
    def fast_update(self, image: Image.Image) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def enter_standby(self) -> None:
        pass
