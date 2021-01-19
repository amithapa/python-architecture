# from datetime import date, timedelta
# from allocation.domain.model import Batch, Product, OrderLine
# from allocation.domain import events
#
# today = date.today()
# tomorrow = today + timedelta(days=1)
# later = tomorrow + timedelta(days=10)
#
# def test_records_out_of_stock_event_if_cannot_allocate():
#     batch = Batch("batch1", "SMALL-FORK", 10, eta=today)
#     product = Product(sku="SMALL-FORK", batches=[batch])
#
#     allocation = product.allocate(OrderLine("order1", "SMALL-FORK", 1))
#     assert product.events[-1] == events.OutOfStock(sku="SMALL-FORK")
#     assert allocation is None