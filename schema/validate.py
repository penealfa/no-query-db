import json
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