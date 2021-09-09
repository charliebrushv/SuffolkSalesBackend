import os

from flask_sqlalchemy import SQLAlchemy
from db import db
import json
from flask import Flask, request
from db import Sale
from datetime import datetime, timedelta
import threading
import time
import pytz
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://"+db_user+":"+db_password+"@"+db_connection_name+"/"+db_name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False


db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

@app.route("/api/sales/", methods=["GET"])
def get_sales():
    return success_response([x.serialize() for x in Sale.query.all()])

@app.route("/api/sales/", methods=["POST"])
def create_sale():
    body = json.loads(request.data)
    if body.get("desc") is None:
        return failure_response("No desc provided", 400)
    if body.get("type") is None:
        return failure_response("No type provided", 400)
    if body.get("lat") is None:
        return failure_response("No latitude provided", 400)
    if body.get("long") is None:
        return failure_response("No longitude provided", 400)
    if body.get("date") is None or body.get("start_time") is None or body.get("end_time") is None:
        return failure_response("No dates provided", 400)
    if body.get("town") is None or body.get("street") is None or body.get("zip") is None:
        return failure_response("No address provided", 400)
    new_sale = Sale(
        desc=body.get("desc"),
        type=body.get("type"),
        lat=str(body.get("lat")),
        long=str(body.get("long")),
        date=body.get("date"),
        start_time=body.get("start_time"),
        end_time=body.get("end_time"),
        street=body.get("street"),
        town=body.get("town"),
        zip=body.get("zip")
    )
    db.session.add(new_sale)
    db.session.commit()
    return success_response(new_sale.serialize(), 201)

@app.route("/api/sales/<int:sale_id>/", methods=["GET"])
def get_sale(sale_id):
    sale = Sale.query.filter_by(id=sale_id).first()
    if sale is None:
        return failure_response("Sale not found")
    return success_response(sale.serialize())

@app.route("/api/sales/<int:sale_id>/", methods=["DELETE"])
def delete_sale(sale_id):
    sale = Sale.query.filter_by(id=sale_id).first()
    if sale is None:
        return failure_response("Sale not found")
    db.session.delete(sale)
    db.session.commit()
    return success_response(sale.serialize())

@app.route("/api/sales/<int:sale_id>/", methods=["POST"])
def edit_sale(sale_id):
    body = json.loads(request.data)
    if body.get("desc") is None:
        return failure_response("No desc provided", 400)
    if body.get("type") is None:
        return failure_response("No type provided", 400)
    if body.get("lat") is None:
        return failure_response("No latitude provided", 400)
    if body.get("long") is None:
        return failure_response("No longitude provided", 400)
    if body.get("date") is None or body.get("start_time") is None or body.get("end_time") is None:
        return failure_response("No dates provided", 400)
    if body.get("town") is None or body.get("street") is None or body.get("zip") is None:
        return failure_response("No address provided", 400)
    sale = Sale.query.filter_by(id=sale_id).first()
    if sale is None:
        return failure_response("Sale not found")
    sale.desc = body.get("desc")
    sale.type = body.get("type")
    sale.lat = body.get("lat")
    sale.long = body.get("long")
    sale.date = body.get("date")
    sale.start_time = body.get("start_time")
    sale.end_time = body.get("end_time")
    sale.town = body.get("town")
    sale.street = body.get("street")
    sale.zip = body.get("zip") 
    
    db.session.commit()
    
    return success_response(sale.serialize())

# yyyy-MM-dd HH:mm:ss
def refresh_data():
    while True:
        with app.app_context():
            for i in Sale.query.all():
                combinedDate = str(i.date)[:11] + str(i.end_time)[11:]
                date = datetime.strptime(combinedDate, "%Y-%m-%d %H:%M:%S")
                date+=timedelta(hours=4)
                if date < datetime.now():
                    # print("deleting")
                    # print("test")
                    # print(str(date)+" < "+str(datetime.now()))
                    # print(str(date)+" < "+str(datetime.now()))
                    db.session.delete(i)
                    db.session.commit()
        time.sleep(60)

        


if __name__ == "__main__":
    thread = threading.Thread(target=refresh_data,daemon=True)
    thread.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


