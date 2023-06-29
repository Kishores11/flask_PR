# Below are installed import
from flask import request, url_for, current_app, Blueprint
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError, DataError, IntegrityError

# Below are custom imports
from app import db
from app.models import Employee
from app.schema import employee_schemas


class NotFoundError(Exception):
    def __init__(self, message, code=404):
        self.message = message
        self.code = code


@current_app.errorhandler(NotFoundError)
def not_found_error(e):
    return {
        "error": f"{e}",
        "message": "The reuqested query could not be found",
    }, 404


employee_api = Blueprint("employee_api", __name__, url_prefix="/")


@employee_api.route("/", methods=["GET"])
@employee_api.route("/<int:id>", methods=["GET"])
def get_employee(id=None):
    try:
        employee_data = Employee.query

        limit = int(request.args.get("limit", current_app.config.get("PAGE_LIMIT")))
        page_num = request.args.get("page", 1, type=int)

        if id:
            employee_data = employee_data.filter(Employee.id == id)
            if employee_data.with_entities(func.count()).scalar() == 0:
                raise NotFoundError("No such employee")

        employee_data = employee_data.paginate(
            page=page_num, per_page=limit, error_out=False
        )

        serialized_data = employee_schemas.dump(employee_data.items)

        next_page_url = None
        if employee_data.has_next:
            next_page_url = url_for(
                "get_employeess",
                page=employee_data.next_num,
                _external=True,
            )

        return {
            "success": True,
            "employee_data": serialized_data,
            "currentPage": employee_data.page,
            "totalPages": employee_data.pages,
            "totalCount": employee_data.total,
            "nextPageUrl": next_page_url,
        }, 200
    except (SQLAlchemyError, DataError, IntegrityError) as e:
        return {"success": False, "message": str(e)}, 500
