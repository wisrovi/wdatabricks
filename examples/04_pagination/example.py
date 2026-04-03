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

    for i in range(1, 21):
        db.insert(User(id=i, name=f"User{i}", email=f"user{i}@example.com"))

    page1 = db.paginate(page=1, page_size=5)
    print(f"Page 1: {len(page1)} users")

    page2 = db.paginate(page=2, page_size=5)
    print(f"Page 2: {len(page2)} users")


if __name__ == "__main__":
    main()
