import pytest
from typing import List, Set
from datetime import date, timedelta

from allocation.domain import model
from allocation.adapters import repository
from allocation.service_layer import services
from allocation.service_layer import unit_of_work


class FakeRepository(repository.AbstractRepository):
    def __init__(self, products: List[model.Product]):
        super().__init__()
        self._products: Set[model.Product] = set(products)

    def _add(self, product: model.Product):
        self._products.add(product)

    def _get(self, sku) -> model.Product:
        return next((p for p in self._products if p.sku == sku), None)

    def list(self) -> List[model.Product]:
        return list(self._products)

today = date.today()
tomrrow = today + timedelta(days=1)
later = today + timedelta(days=2)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):

    def __init__(self):
        self.products = FakeRepository([])
        self.committed = False

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass

def test_prefers_warehouse_batches_to_shipments():
    uow = FakeUnitOfWork()
    services.add_batch("in-stock-batch", "RETRO-CLOCK", 100, None, uow)
    services.add_batch("shipment-batch", "RETRO-CLOCK", 100, tomrrow, uow)

    services.allocate("oref", "RETRO-CLOCK", 10, uow)
    products = uow.products.get("RETRO-CLOCK")

    in_stock_batch = products.batches[0]
    shipment_batch = products.batches[1]

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100

def test_add_batch_for_new_product():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "CRUNCHY=ARMCHAIR", 100, None, uow)
    assert uow.products.get("CRUNCHY=ARMCHAIR") is not None
    assert uow.committed

def test_add_batch_for_existing_product():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "GARISH-RUG", 100, None, uow)
    services.add_batch("b2", "GARISH-RUG", 99, None, uow)
    assert "b2" in [b.reference for b in uow.products.get("GARISH-RUG").batches]

def test_allocate_returns_allocation():
    uow = FakeUnitOfWork()
    services.add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)
    result = services.allocate("o1", "COMPLICATED-LAMP", 10, uow)
    assert result == "batch1"


def test_allocate_error_for_invalid_sku():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "AREALSKU", 100, None, uow)
    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        services.allocate("o1", "NONEXISTENTSKU", 10, uow)

def test_allocate_commits():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "OMINOUS-MIRROR", 100, None, uow)
    services.allocate("o1", "OMINOUS-MIRROR", 10, uow)
    assert uow.committed is True
