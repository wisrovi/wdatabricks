from typing import Optional
from pydantic import BaseModel
from wdatabricks import WDatabricks

DB_CONFIG = {
    "server_hostname": "your-server.cloud.databricks.com",
    "http_path": "/sql/your-http-path",
    "access_token": "your-access-token",
}


class User(BaseModel):
    id: int
    name: str
    age: int


def main():
    db = WDatabricks(User, DB_CONFIG)
    db.insert(User(id=1, name="Alice", age=25))
    print(f"Initial users: {db.get_all()}")


class UserExtended(BaseModel):
    id: int
    name: str
    age: int
    email: Optional[str] = None


def main_extended():
    db = WDatabricks(UserExtended, DB_CONFIG)
    db.insert(UserExtended(id=2, name="Bob", age=30, email="bob@example.com"))
    print(f"Users with new column: {db.get_all()}")


if __name__ == "__main__":
    main()
