import abc
from allocation.domain import model
from typing import List


class AbstractRepository(abc.ABC):

    def __init__(self):
        self.seen = set()

    def add(self, product: model.Product):
        self._add(product)
        self.seen.add(product)

    def get(self, sku) -> model.Product:
        product = self._get(sku)
        if product:
            self.seen.add(product)
        return product

    @abc.abstractmethod
    def _add(self, product: model.Product):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku) -> model.Product:
        raise NotImplementedError

    # @abc.abstractmethod
    # def list(self) -> List[model.Batch]:
    #     raise NotImplementedError

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.__session = session

    def _add(self, product: model.Product):
        self.__session.add(product)

    def _get(self, sku) -> model.Product:
        return self.__session.query(model.Product).filter_by(sku=sku).first()

    # def list(self):
    #     return self.__session.query(model.Product).all()
