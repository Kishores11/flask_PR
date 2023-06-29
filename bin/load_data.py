import os
import sys
import requests

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(parentdir)
sys.path.insert(0, parentdir)

from app import db
from app.models import Employee


def create_object_in_db_at_startup():
    # Read the data from load.json
    response = requests.get(
        "https://api.slingacademy.com/v1/sample-data/files/employees.json"
    )
    data = response.json()

    # Iterate over the employee objects and insert them into the database
    for employee_data in data["employees"]:
        employee = Employee(
            id=employee_data["id"],
            first_name=employee_data["first_name"],
            last_name=employee_data["last_name"],
            age=employee_data["age"],
            salary=employee_data["salary"],
        )
        db.session.add(employee)

    # Commit the changes to the database
    db.session.commit()

    print("Data loaded successfully")


create_object_in_db_at_startup()
