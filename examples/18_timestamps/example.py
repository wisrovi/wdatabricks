from datetime import datetime
from pydantic import BaseModel
from wdatabricks import WDatabricks

DB_CONFIG = {
    "server_hostname": "your-server.cloud.databricks.com",
    "http_path": "/sql/your-http-path",
    "access_token": "your-access-token",
}


class Record(BaseModel):
    id: int
    data: str
    created_at: str = datetime.now().isoformat()


def main():
    db = WDatabricks(Record, DB_CONFIG)
    db.insert(Record(id=1, data="Test"))
    record = db.get_by_field(id=1)[0]
    print(f"Record: {record}")


if __name__ == "__main__":
    main()
