import pytest
from typing import List, Set
from datetime import date, timedelta

from allocation.domain import model
from allocation.adapters import repository
from allocation.service_layer import services
from allocation.service_layer import unit_of_work


class FakeRepository(repository.AbstractRepository):
    def __init__(self, batches: List[model.Batch]):
        self._batches: Set[model.Batch] = set(batches)

    def add(self, batch: model.Batch):
        self._batches.add(batch)

    def get(self, reference) -> model.Batch:
        return next(b for b in self._batches if b.reference == reference)

    def list(self) -> List[model.Batch]:
        return list(self._batches)

today = date.today()
tomrrow = today + timedelta(days=1)
later = today + timedelta(days=2)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):

    def __init__(self):
        self.batches = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_prefers_warehouse_batches_to_shipments():
    uow = FakeUnitOfWork()
    services.add_batch("in-stock-batch", "RETRO-CLOCK", 100, None, uow)
    services.add_batch("shipment-batch", "RETRO-CLOCK", 100, tomrrow, uow)

    in_stock_batch = uow.batches.get("in-stock-batch")
    shipment_batch = uow.batches.get("shipment-batch")
    services.allocate("oref", "RETRO-CLOCK", 10, uow)

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_add_batch():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "CRUNCHY=ARMCHAIR", 100, None, uow)
    assert uow.batches.get("b1") is not None
    assert uow.committed

def test_allocate_returns_allocation():
    uow = FakeUnitOfWork()
    services.add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)
    result = services.allocate("o1", "COMPLICATED-LAMP", 10, uow)
    assert result == "batch1"


def test_error_for_invalid_sku():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "AREALSKU", 100, None, uow)
    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        services.allocate("o1", "NONEXISTENTSKU", 10, uow)

def test_commits():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "OMINOUS-MIRROR", 100, None, uow)
    services.allocate("o1", "OMINOUS-MIRROR", 10, uow)
    assert uow.committed is True
