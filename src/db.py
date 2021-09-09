from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import os

db = SQLAlchemy()

class Sale(db.Model):    
    __tablename__ = "sale"    
    id = db.Column(db.Integer, primary_key=True)      
    desc = db.Column(db.String, nullable=False)    
    type = db.Column(db.String, nullable=False)
    lat = db.Column(db.String, nullable=False)
    long = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)    
    start_time = db.Column(db.String, nullable=False)
    end_time = db.Column(db.String, nullable=False)
    street = db.Column(db.String, nullable=False)    
    town = db.Column(db.String, nullable=False)
    zip = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.desc = kwargs.get("desc")
        self.type = kwargs.get("type")
        self.lat = kwargs.get("lat")
        self.long = kwargs.get("long")
        self.date = kwargs.get("date")
        self.start_time = kwargs.get("start_time")
        self.end_time = kwargs.get("end_time")
        self.street = kwargs.get("street")
        self.town = kwargs.get("town")
        self.zip = kwargs.get("zip")

    def serialize(self):
        return {
            "id": self.id,
            "desc": self.desc,
            "type": self.type,
            "lat": float(self.lat),
            "long": float(self.long),
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "street": self.street,
            "town": self.town,
            "zip": self.zip
        }
