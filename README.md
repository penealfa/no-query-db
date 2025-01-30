# NoqueryDB Documentation

NoqueryDB is a lightweight, JSON-based database system with a Python CLI and ORM. It allows users to define their database schema using JSON files and interact with the database using Python classes. This documentation covers the current features of NoqueryDB, with more features to come in future updates.

---

## Table of Contents
1. [Installation](#installation)
2. [Getting Started](#getting-started)
   - [Defining the Schema](#defining-the-schema)
   - [Initializing the Database](#initializing-the-database)
3. [Using the ORM](#using-the-orm)
   - [Defining Models](#defining-models)
   - [Inserting Data](#inserting-data)
   - [Querying Data](#querying-data)
4. [CLI Commands](#cli-commands)
5. [Future Features](#future-features)

---

## Installation (when it's distributed)

To install NoqueryDB, use `pip`:

```bash
pip install noquerydb
```

---

## Getting Started

### Defining the Schema

NoqueryDB uses two JSON files to define the database schema so create this files in a folder named database so that the cli can find it:
1. **`main.json`**: Defines the database name.
2. **`tables.json`**: Defines the tables and their columns.

#### Example `main.json`
```json
{
    "name": "MyFirstDB"
}
```

#### Example `tables.json`
```json
{
    "databaseName": "MyFirstDB",
    "tables": [
        {
            "name": "users",
            "columns": [
                {
                    "name": "id",
                    "type": "INT",
                    "constraints": ["PRIMARY KEY", "NOT NULL", "AUTO_INCREMENT"]
                },
                {
                    "name": "name",
                    "type": "VARCHAR(255)",
                    "constraints": ["NOT NULL"]
                },
                {
                    "name": "email",
                    "type": "VARCHAR(255)",
                    "constraints": ["NOT NULL", "UNIQUE"]
                },
                {
                    "name": "created_at",
                    "type": "TIMESTAMP",
                    "constraints": ["DEFAULT CURRENT_TIMESTAMP"]
                }
            ]
        }
    ]
}
```

### Initializing the Database

Use the CLI to initialize the database with the schema files:

```bash
noquerydb crdb
```

This command creates a `.db` file (e.g., `MyFirstDB.db`) that stores the database structure and data.

---

### Initializing the tables

Use the CLI to initialize the database with the schema files:

```bash
noquerydb createtable
```

This command creates the tables in the database file.

---

## Using the ORM

NoqueryDB provides an ORM to interact with the database using Python classes.

### Defining Models

Create a Python class that inherits from `BaseModel` and maps to a table in your database:

```python
from orm import BaseModel

class User(BaseModel):
    _database_name = "MyFirstDB"  # From main.json
    _table_name = "users"         # From tables.json
```

### Inserting Data

You can insert data into the database using the `save()` method. The ORM will automatically handle:
- Auto-incrementing primary keys.
- Default timestamps for `created_at`.

```python
# No need to provide `id` or `created_at`; they will be auto-generated
user = User(name="Peneal", email="peneal@example.com")
user.save()
```

### Querying Data

Use the `objects()` method to retrieve all rows from a table:

```python
all_users = User.objects()
print(all_users)
```

**Output:**
```json
[
    {
        "id": 1,
        "name": "Peneal",
        "email": "peneal@example.com",
        "created_at": "2025-01-30 14:30:00"
    }
]
```

---

## CLI Commands

NoqueryDB provides the following CLI commands for now:

| Command                | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `noquerydb crdb`       | Initialize the database using `main.json`.                                  |
| `noquerydb createtable`| Initialize the tables using `tables.json`.                                  |
| `noquerydb showtables` | Displays all the tables created in the .db file.                            |

---

## Future Features

NoqueryDB is under active development. Here are some planned features:

1. **Query Filters**:
   - Support for filtering data (e.g., `User.objects.filter(name="Peneal")`).

2. **Data Validation**:
   - Advanced validation for data types and constraints.

3. **Indexing**:
   - Add support for indexing to improve query performance.

4. **Transactions**:
   - Support for transactions (e.g., rollback on failure).

5. **API Integration**:
   - Expose the database via a REST API.

6. **CLI Enhancements**:
   - Add commands for updating and deleting data.

---

## Contributing

Contributions are welcome! If you'd like to contribute to NoqueryDB, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request.

---

## License

NoqueryDB is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support

For questions, issues, or feature requests, please open an issue on the [GitHub repository](https://github.com/penealfa/no-query-db).

---

This documentation will be updated as new features are added to NoqueryDB. Stay tuned for more! 🚀
