# import pytest
# from typing import List, Set
# from datetime import date, timedelta
#
# from allocation.domain import model
# from allocation.domain import events
# from allocation.adapters import repository
# from allocation.service_layer import handlers
# from allocation.service_layer import unit_of_work
#
#
# class FakeRepository(repository.AbstractRepository):
#     def __init__(self, products: List[model.Product]):
#         super().__init__()
#         self._products: Set[model.Product] = set(products)
#
#     def _add(self, product: model.Product):
#         self._products.add(product)
#
#     def _get(self, sku) -> model.Product:
#         return next((p for p in self._products if p.sku == sku), None)
#
#     def list(self) -> List[model.Product]:
#         return list(self._products)
#
#     def _get_by_batchref(self, batchref):
#         return next((
#             p for p in self._products for b in p.batches
#             if b.reference == batchref
#         ), None)
#
# today = date.today()
# tomrrow = today + timedelta(days=1)
# later = today + timedelta(days=2)
#
#
# class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
#
#     def __init__(self):
#         self.products = FakeRepository([])
#         self.committed = False
#
#     def _commit(self):
#         self.committed = True
#
#     def rollback(self):
#         pass
#
# def test_prefers_warehouse_batches_to_shipments():
#     uow = FakeUnitOfWork()
#     handlers.add_batch("in-stock-batch", "RETRO-CLOCK", 100, None, uow)
#     handlers.add_batch("shipment-batch", "RETRO-CLOCK", 100, tomrrow, uow)
#
#     handlers.allocate("oref", "RETRO-CLOCK", 10, uow)
#     products = uow.products.get("RETRO-CLOCK")
#
#     in_stock_batch = products.batches[0]
#     shipment_batch = products.batches[1]
#
#     assert in_stock_batch.available_quantity == 90
#     assert shipment_batch.available_quantity == 100
#
# def test_add_batch_for_new_product():
#     uow = FakeUnitOfWork()
#     handlers.add_batch("b1", "CRUNCHY=ARMCHAIR", 100, None, uow)
#     assert uow.products.get("CRUNCHY=ARMCHAIR") is not None
#     assert uow.committed
#
# def test_add_batch_for_existing_product():
#     uow = FakeUnitOfWork()
#     handlers.add_batch("b1", "GARISH-RUG", 100, None, uow)
#     handlers.add_batch("b2", "GARISH-RUG", 99, None, uow)
#     assert "b2" in [b.reference for b in uow.products.get("GARISH-RUG").batches]
#
# def test_allocate_returns_allocation():
#     uow = FakeUnitOfWork()
#     handlers.add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)
#     result = handlers.allocate("o1", "COMPLICATED-LAMP", 10, uow)
#     assert result == "batch1"
#
#
# def test_allocate_error_for_invalid_sku():
#     uow = FakeUnitOfWork()
#     handlers.add_batch("b1", "AREALSKU", 100, None, uow)
#     with pytest.raises(handlers.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
#         handlers.allocate("o1", "NONEXISTENTSKU", 10, uow)
#
# def test_allocate_commits():
#     uow = FakeUnitOfWork()
#     handlers.add_batch("b1", "OMINOUS-MIRROR", 100, None, uow)
#     handlers.allocate("o1", "OMINOUS-MIRROR", 10, uow)
#     assert uow.committed is True
