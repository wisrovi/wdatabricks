import asyncio
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


async def main():
    db = WDatabricks(User, DB_CONFIG)
    await db.insert_async(User(id=3, name="Bob", email="bob@example.com"))
    users = await db.get_all_async()
    print(users)


if __name__ == "__main__":
    asyncio.run(main())
