import abc
from allocation.domain import model
from typing import List


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, product: model.Product):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, sku) -> model.Product:
        raise NotImplementedError

    # @abc.abstractmethod
    # def list(self) -> List[model.Batch]:
    #     raise NotImplementedError

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.__session = session

    def add(self, product: model.Product):
        self.__session.add(product)

    def get(self, sku) -> model.Product:
        return self.__session.query(model.Product).filter_by(sku=sku).first()

    # def list(self):
    #     return self.__session.query(model.Product).all()
