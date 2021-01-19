from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from allocation import config
from allocation.domain import model
from allocation.domain import events
from allocation.adapters import orm, repository
from allocation.service_layer import handlers
from allocation.service_layer import unit_of_work
from allocation.service_layer import messagebus

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)

@app.route("/allocate", methods=["POST"])
def allocation_endpoint():
    try:
        event = events.AllocationRequired(
            request.json["orderid"], request.json["sku"], request.json["qty"]
        )
        results = messagebus.handle(event, unit_of_work.SqlAlchemyUnitOfWork())
        batchref = results.pop(0)
    except (model.OutOfStock, handlers.InvalidSku) as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"batchref": batchref}), 201

@app.route("/add_batch", methods=["POST"])
def add_batch():
    eta = request.json["eta"]
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    event = events.BatchCreated(request.json["ref"], request.json["sku"], request.json["qty"], eta)
    messagebus.handle(event, unit_of_work.SqlAlchemyUnitOfWork())
    return "OK", 201