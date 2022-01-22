import abc

STAGES: dict[str, any] = {}


class StageBase(abc.ABC):
    @abc.abstractmethod
    def __init__(self, *args: [str]):
        pass

    @abc.abstractmethod
    def process(self) -> [str]:
        pass

    @staticmethod
    @abc.abstractmethod
    def help() -> str:
        pass


def register_stage(name):
    def wrapper(cls):
        STAGES[name] = cls
        return cls
    return wrapper
