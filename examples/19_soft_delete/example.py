from typing import Optional
from pydantic import BaseModel, Field
from wdatabricks import WDatabricks

DB_CONFIG = {
    "server_hostname": "your-server.cloud.databricks.com",
    "http_path": "/sql/your-http-path",
    "access_token": "your-access-token",
}


class User(BaseModel):
    id: int
    name: str
    deleted: Optional[int] = Field(default=0)


def main():
    db = WDatabricks(User, DB_CONFIG)

    db.insert(User(id=1, name="Alice"))
    db.insert(User(id=2, name="Bob"))

    print(f"Total: {db.count()}")
    user = db.get_by_field(id=1)[0]
    db.update(1, User(id=1, name=user.name, deleted=1))
    print(f"After soft delete: {db.count()}")


if __name__ == "__main__":
    main()
