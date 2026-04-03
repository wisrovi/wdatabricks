import logging
from pydantic import BaseModel
from wdatabricks import WDatabricks

logging.basicConfig(level=logging.DEBUG)

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
    db = WDatabricks(User, DB_CONFIG, log_level=logging.DEBUG)
    db.sync.create_if_not_exists()

    db.insert(User(id=1, name="LoggedUser", email="logged@example.com"))
    print("Logged operation completed")


if __name__ == "__main__":
    main()
