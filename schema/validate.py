import json
import re
from jsonschema import validate, exceptions

def load_schema(file_path):
    with open(file_path,'r') as f:
        return json.load(f)
    

def validate_data(data, schema):
    schema_json = load_schema(schema)
    try:
        validate(instance=data, schema=schema_json)
        print("Data is valid!")
    except exceptions.ValidationError as e:
        print(f"Validation error: {e.message}")
        print(f"Error path: {e.path}")
    except exceptions.SchemaError as e:
        print(f"Schema error: {e.message}")

def validate_table_schema(tables_data):
    # Check if 'databaseName' is present and is a string
    if 'databaseName' not in tables_data or not isinstance(tables_data['databaseName'], str):
        return False
    
    # Check if 'tables' is present and is a list
    if 'tables' not in tables_data or not isinstance(tables_data['tables'], list):
        return False
    
    # Define a set of valid data types
    valid_data_types = {
        'TINYINT', 'SMALLINT', 'MEDIUMINT', 'INT', 'INTEGER', 'BIGINT',
        'DECIMAL', 'NUMERIC', 'FLOAT', 'DOUBLE', 'DOUBLE PRECISION', 'REAL',
        'BIT',
        'CHAR', 'VARCHAR', 'TINYTEXT', 'TEXT', 'MEDIUMTEXT', 'LONGTEXT',
        'DATE', 'TIME', 'DATETIME', 'TIMESTAMP', 'YEAR',
        'BOOLEAN', 'BOOL'
    }
    
    # Define a set of valid constraints
    valid_constraints = {
        'PRIMARY KEY', 'NOT NULL', 'AUTO_INCREMENT', 'UNIQUE',
        'DEFAULT CURRENT_TIMESTAMP', 'FOREIGN KEY'
    }
    
    # Validate each table
    for table in tables_data['tables']:
        # Check if 'name' is present and is a string
        if 'name' not in table or not isinstance(table['name'], str):
            return False
        
        # Check if 'columns' is present and is a list
        if 'columns' not in table or not isinstance(table['columns'], list):
            return False
        
        # Validate each column
        for column in table['columns']:
            # Check if 'name' is present and is a string
            if 'name' not in column or not isinstance(column['name'], str):
                return False
            
            # Check if 'type' is present and is a valid data type
            if 'type' not in column or not isinstance(column['type'], str):
                return False
            
            # Handle parameterized types like DECIMAL(p, s) and VARCHAR(n)
            column_type = column['type'].upper()
            if column_type.startswith('DECIMAL') or column_type.startswith('NUMERIC'):
                match = re.match(r'DECIMAL\((\d+),(\d+)\)', column_type)
                if not match:
                    return False
            elif column_type.startswith('VARCHAR'):
                match = re.match(r'VARCHAR\((\d+)\)', column_type)
                if not match:
                    return False
            elif column_type.startswith('CHAR'):
                match = re.match(r'CHAR\((\d+)\)', column_type)
                if not match:
                    return False
            elif column_type not in valid_data_types:
                return False
            
            # Check if 'constraints' is present and is a list
            if 'constraints' not in column or not isinstance(column['constraints'], list):
                return False
            
            # Validate each constraint
            for constraint in column['constraints']:
                if constraint not in valid_constraints:
                    return False
    
    return True