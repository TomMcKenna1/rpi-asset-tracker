from .base import Display


class DisplayFactory:
    _registry = {}

    @classmethod
    def register(cls, name):
        def wrapper(class_obj):
            if name in cls._registry:
                raise ValueError(f"{name} already exists in display registry.")
            else:
                cls._registry[name] = class_obj
            return class_obj

        return wrapper

    @classmethod
    def get(cls, name: str) -> Display:
        return cls._registry[name]()
