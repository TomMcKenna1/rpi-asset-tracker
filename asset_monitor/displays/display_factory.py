from .base import Display


class DisplayDoesNotExist(Exception):
    pass


class DisplayFactory:
    """
    Factory class to manage display classes.
    """

    _registry = {}

    @classmethod
    def register(cls, id):
        def wrapper(class_obj):
            if id in cls._registry:
                raise ValueError(f"{id} already exists in display registry.")
            else:
                cls._registry[id] = class_obj
            return class_obj

        return wrapper

    @classmethod
    def get(cls, id: str) -> Display:
        display = cls._registry.get(id)
        if display:
            return display()
        else:
            raise DisplayDoesNotExist(
                f"No display '{id}' implementaton found. Please use the DisplayFactory.register decorator to register a display implementation."
            )
