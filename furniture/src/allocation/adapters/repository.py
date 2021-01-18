import abc
from allocation.domain import model
from typing import List


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[model.Batch]:
        raise NotImplementedError

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.__session = session

    def add(self, batch: model.Batch):
        self.__session.add(batch)

    def get(self, reference) -> model.Batch:
        return self.__session.query(model.Batch).filter_by(reference=reference).one()

    def list(self):
        return self.__session.query(model.Batch).all()
