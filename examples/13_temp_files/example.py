import os
import tempfile
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

    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt")
    temp_file.write("Temp data\n")
    temp_file.close()

    db.insert(User(id=1, name="TempUser", email="temp@example.com"))
    users = db.get_all()
    print(f"Users: {len(users)}")

    os.unlink(temp_file.name)


if __name__ == "__main__":
    main()
