from abc import abstractmethod, ABC

from storage import SQLiteClient


class GenericContainer(ABC):
    def __init__(self, client: SQLiteClient):
        # TODO : something to do with this?
        pass

    @abstractmethod
    def get_or_create(self, *args, **kwargs):
        pass
