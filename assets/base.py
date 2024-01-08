from abc import ABC, abstractmethod

class Asset(ABC):

    @property
    @abstractmethod
    def name(self):
        pass
    
    @property 
    @abstractmethod
    def price(self):
        pass

    @abstractmethod
    def get_latest_price(self):
        pass