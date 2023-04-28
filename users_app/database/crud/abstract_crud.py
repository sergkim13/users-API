from abc import ABC, abstractmethod


class AbstractCRUD(ABC):
    '''Abstract CRUD class.'''
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def read_all(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def read(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def create(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs):
        raise NotImplementedError
