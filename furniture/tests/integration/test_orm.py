from datetime import date
from domain import model


def test_orderline_mapper_can_load_lines(session):
    session.execute(
        "INSERT INTO order_lines (orderid, sku, qty) VALUES "
        "('order1', 'RED-CHAIR', 12),"
        "('order1', 'RED-CHAIR', 13),"
        "('order1', 'BLUE-LIPSTICK', 14)"
    )
    expected = [
        model.OrderLine("order1", "RED-CHAIR", 12),
        model.OrderLine("order1", "RED-CHAIR", 13),
        model.OrderLine("order1", "BLUE-LIPSTICK", 14),
    ]
    assert session.query(model.OrderLine).all() == expected

def test_orderline_mapper_can_save_lines(session):
    new_line = model.OrderLine("order1", "DECORATIVE-WIDGET", 12)
    session.add(new_line)
    session.commit()

    rows = list(session.execute("SELECT orderid, sku, qty FROM 'order_lines'"))
    assert rows == [(new_line.orderid, new_line.sku, new_line.qty)]

def test_retrieving_batches(session):
    session.execute(
        "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
        " VALUES ('batch1', 'sku1', 100, null)"
    )
    session.execute(
        "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
        " VALUES ('batch2', 'sku2', 200, '2019-03-28')"
    )
    expected = [
        model.Batch("batch1", "sku1", 100, None),
        model.Batch("batch2", "sku2", 200, date(2019, 3, 28)),
    ]

    assert session.query(model.Batch).all() == expected

def test_saving_batches(session):
    batch = model.Batch("batch1", "sku1", 100, eta=None)
    session.add(batch)
    session.commit()
    rows = list(session.execute(
        "SELECT reference, sku, _purchased_quantity, eta FROM 'batches'"
    ))
    assert rows == [(batch.reference, batch.sku, batch._purchased_quantity, batch.eta)]

def test_saving_allocations(session):
    batch = model.Batch("batch1", "sku1", 100, eta=None)
    line = model.OrderLine("order1", "sku1", 10)
    batch.allocate(line)
    session.add(batch)
    session.commit()
    rows = list(session.execute("SELECT orderline_id, batch_id FROM 'allocations'"))
    assert rows == [(batch.id, line.id)]