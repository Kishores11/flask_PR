from app import db
from dataclasses import dataclass


@dataclass
class Employee(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name: str = db.Column(db.Text, unique=True, nullable=False)
    last_name: str = db.Column(db.Text, unique=True, nullable=False)
    age: int = db.Column(db.Integer, nullable=False)
    salary: int = db.Column(db.Integer, nullable=False)
