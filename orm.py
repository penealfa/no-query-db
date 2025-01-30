import os
import pickle
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime  # For handling timestamps

class NoqueryDB:
    _databases: Dict[str, Any] = {}
    
    @classmethod
    def get_database(cls, name: str) -> Dict[str, Any]:
        """Load the database from the .db file."""
        db_path = Path(f"{name}.db")
        if not db_path.exists():
            raise FileNotFoundError(f"Database '{name}' does not exist. Run CLI to create it first.")
        with open(db_path, "rb") as db_file:
            return pickle.load(db_file)

    @classmethod
    def save_database(cls, name: str, data: Dict[str, Any]):
        """Save the database to the .db file."""
        db_path = Path(f"{name}.db")
        with open(db_path, "wb") as db_file:
            pickle.dump(data, db_file)

class BaseModel:
    _database_name: str = None
    _table_name: str = None

    def __init__(self, **kwargs):
        self._validate_schema()
        self._set_attributes(kwargs)

    def _validate_schema(self):
        """Validate the model against the database schema."""
        if not self._database_name or not self._table_name:
            raise ValueError("Model must define _database_name and _table_name.")
        
        db = NoqueryDB.get_database(self._database_name)
        if self._table_name not in db['tables']:
            raise ValueError(f"Table '{self._table_name}' does not exist.")
        
        self._schema = db['tables'][self._table_name]['columns']

    def _set_attributes(self, data: Dict[str, Any]):
        """Set attributes based on the table schema."""
        for column in self._schema:
            col_name = column['name']
            value = data.get(col_name)

            # Handle NOT NULL constraints (except for auto-generated fields)
            if (
                'NOT NULL' in column.get('constraints', [])
                and value is None
                and 'AUTO_INCREMENT' not in column.get('constraints', [])
                and 'DEFAULT' not in column.get('constraints', [])
            ):
                raise ValueError(f"{col_name} cannot be NULL.")
            
            setattr(self, col_name, value)

    def save(self):
        """Save the instance to the database."""
        db = NoqueryDB.get_database(self._database_name)
        table = db['tables'][self._table_name]

        # Prepare row data
        row = {}
        for column in self._schema:
            col_name = column['name']
            value = getattr(self, col_name, None)

            # Handle auto-increment for primary keys
            if 'AUTO_INCREMENT' in column.get('constraints', []):
                if value is None:  # Only auto-generate if not provided
                    current_max = max(row.get(col_name, 0) for row in table.get('rows', [])) if table.get('rows') else 0
                    value = current_max + 1
                setattr(self, col_name, value)

            # Handle default timestamp for created_at
            if col_name == "created_at" and value is None:
                value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                setattr(self, col_name, value)

            row[col_name] = value

        # Save to DB
        if 'rows' not in table:
            table['rows'] = []
        table['rows'].append(row)

        NoqueryDB.save_database(self._database_name, db)
        return row

    @classmethod
    def objects(cls) -> List[Dict[str, Any]]:
        """Get all rows from the table."""
        db = NoqueryDB.get_database(cls._database_name)
        return db['tables'][cls._table_name].get('rows', [])