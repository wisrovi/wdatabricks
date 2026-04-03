from pydantic import BaseModel
from wdatabricks import WDatabricks

DB_CONFIG = {
    "server_hostname": "your-server.cloud.databricks.com",
    "http_path": "/sql/your-http-path",
    "access_token": "your-access-token",
}


class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: float


def main():
    db = WDatabricks(Employee, DB_CONFIG)
    db.sync.create_if_not_exists()

    employees = [
        Employee(id=1, name="Alice", department="IT", salary=70000),
        Employee(id=2, name="Bob", department="IT", salary=75000),
    ]
    for emp in employees:
        db.insert(emp)

    result = db.execute_raw(
        "SELECT name, salary, ROW_NUMBER() OVER (ORDER BY salary DESC) as rn FROM employees"
    )
    print(f"Window function: {result}")


if __name__ == "__main__":
    main()
