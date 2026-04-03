from pydantic import BaseModel
from wdatabricks import WDatabricks

DB_CONFIG = {
    "server_hostname": "your-server.cloud.databricks.com",
    "http_path": "/sql/your-http-path",
    "access_token": "your-access-token",
}


class Author(BaseModel):
    id: int
    name: str


class Book(BaseModel):
    id: int
    title: str
    author_id: int


def main():
    author_db = WDatabricks(Author, DB_CONFIG)
    book_db = WDatabricks(Book, DB_CONFIG)

    author_db.insert(Author(id=1, name="Alice"))
    book_db.insert(Book(id=1, title="Book 1", author_id=1))

    print(f"Authors: {author_db.get_all()}")
    print(f"Books: {book_db.get_all()}")


if __name__ == "__main__":
    main()
