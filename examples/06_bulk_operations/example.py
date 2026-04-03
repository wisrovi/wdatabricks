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
    email: str


def main():
    db = WDatabricks(User, DB_CONFIG)
    db.sync.create_if_not_exists()

    users = [
        User(id=i, name=f"BulkUser{i}", email=f"bulk{i}@example.com")
        for i in range(1, 11)
    ]
    db.bulk_insert(users)
    print(f"Bulk inserted {len(users)} users")

    db.bulk_update(users)
    print("Bulk updated users")


if __name__ == "__main__":
    main()
