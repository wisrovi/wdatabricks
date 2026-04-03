import pytest
from pydantic import BaseModel


class TestConnection:
    def test_import(self):
        from wdatabricks.core.connection import ConnectionManager

        assert ConnectionManager is not None


class TestRepository:
    def test_import(self):
        from wdatabricks.core.repository import Repository

        assert Repository is not None

    def test_model_validation(self):
        from wdatabricks.core.repository import Repository

        class User(BaseModel):
            id: int
            name: str

        repo = Repository(User)
        assert repo.model == User
