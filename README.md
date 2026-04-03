# wdatabricks

**Databricks SQL ORM library for Python - type-safe database operations**

High-level Python ORM library providing a clean, type-safe interface for Databricks SQL operations using Pydantic models for schema definition.

## Key Features

- **Pydantic Integration** - Define database schema using Pydantic models
- **Auto Table Creation** - Tables created/synchronized automatically with model changes
- **CRUD Operations** - Simple insert, get, update, delete methods
- **Type Safety** - Full type hints and Pydantic validation
- **Async Support** - Full async/await for high-performance applications
- **Query Builder** - Safe query construction with SQL injection prevention
- **CLI Tool** - Command-line interface for common operations
- **Code Quality** - Pylint compatible, comprehensive type hints

## Technical Stack

- **Python**: 3.8+
- **Key Libraries**: databricks-sql-connector>=2.0.0
- **Testing**: pytest, pytest-cov, pytest-asyncio
- **Code Quality**: black, flake8, mypy

## Installation & Setup

```bash
pip install wdatabricks
```

Development installation:
```bash
pip install -e ".[dev]"
```

## Architecture & Workflow

```
wdatabricks/
├── src/wdatabricks/       # Main library package
│   ├── core/              # Core database operations
│   ├── builders/          # SQL query builder
│   ├── exceptions/       # Custom exceptions
│   ├── types/            # SQL type mapping
│   └── cli/              # CLI tool
├── examples/              # Usage examples (13+ folders)
├── test/                  # Test suite
│   ├── unit/            # Unit tests
│   └── integration/    # Integration tests
├── docs/                  # Sphinx documentation
├── stress_test/          # Performance testing
├── docker/               # Docker configurations
├── pyproject.toml        # Project config
└── README.md
```

**Workflow**: Define Pydantic model → Configure Databricks connection → Initialize WDatabricks → Perform CRUD operations

## Configuration

**Environment Variables**:
- `DATABRICKS_SERVER_HOSTNAME` - Server hostname
- `DATABRICKS_HTTP_PATH` - HTTP path
- `DATABRICKS_ACCESS_TOKEN` - Access token

**Configuration Files**:
- `pyproject.toml` - Project metadata and dependencies
- `setup.py` - Package configuration

## Usage

```python
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

db = WDatabricks(User, DB_CONFIG)
db.insert(User(id=1, name="John", email="john@example.com"))
users = db.get_all()
```

## Author

- **William Rodríguez** - [wisrovi.rodriguez@gmail.com](mailto:wisrovi.rodriguez@gmail.com)
- [LinkedIn](https://www.linkedin.com/in/wisrovi/)