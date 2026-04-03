import pytest
from pydantic import BaseModel
from wdatabricks.core.sync import TableSync


class TestTableSync:
    def test_import(self):
        from wdatabricks.core.sync import TableSync

        assert TableSync is not None

    def test_sync_creation(self):
        from wdatabricks.core.sync import TableSync

        class User(BaseModel):
            id: int
            name: str

        sync = TableSync(User, {})
        assert sync.model == User
