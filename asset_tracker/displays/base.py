from abc import ABC, abstractmethod

from PIL import Image


class Display(ABC):
    @abstractmethod
    def get_width(self) -> int:
        pass

    @abstractmethod
    def get_height(self) -> int:
        pass

    @abstractmethod
    def update(self, image: Image.Image):
        pass

    @abstractmethod
    def enter_standby(self):
        pass
