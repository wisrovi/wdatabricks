from pydantic import BaseModel
from wdatabricks import WDatabricks, QueryBuilder

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

    db.insert(User(id=1, name="John", email="john@example.com"))
    db.insert(User(id=2, name="Jane", email="jane@example.com"))

    subquery = QueryBuilder().select("MAX(id)").from_table("users").build()
    query = (
        QueryBuilder()
        .select("*")
        .from_table("users")
        .where(f"id = ({subquery})")
        .build()
    )
    print(f"Subquery: {query}")


if __name__ == "__main__":
    main()
