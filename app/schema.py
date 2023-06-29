from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app import app
from app.models import Employee

ma = Marshmallow(app)


class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee


employee_schemas = EmployeeSchema(many=True)
