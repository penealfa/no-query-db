import click
import pickle
import json
import os
from schema.validate import validate_data, validate_table_schema
from pathlib import Path

@click.group()
def cli():
    pass

@cli.command()
def crdb():
    json_path = os.path.join("database", "main.json")
    if not os.path.exists(json_path):
        click.echo(f"Error: The file '{json_path}' does not exist.")
        return
    try:
        with open(json_path, "r") as file:
            data = json.load(file)
            validate_data=(data,'./schema/database')
            if 'name' in data:
                db_name = data['name']
                db_path = Path(f"{db_name}.db")
                tables= {}
                with open(db_path, "wb") as db_file:
                    pickle.dump({"tables": tables},db_file)
                click.echo(f"Database '{db_name}' created.")
    except json.JSONDecodeError as e:
        click.echo(f"Error: Failed to parse JSON file. {e}")


@cli.command()
def createtable():
    tables_json_path = os.path.join("database", "tables.json")
    
    if not os.path.exists(tables_json_path):
        click.echo(f"Error: The file '{tables_json_path}' does not exist.")
        return
    
    try:
        with open(tables_json_path, "r") as file:
            tables_data = json.load(file)
            if not validate_table_schema(tables_data):
                click.echo("Error: Invalid table schema.")
                return
            
            db_name = tables_data.get('databaseName')
            if not db_name:
                click.echo("Error: 'databaseName' not found in tables.json.")
                return
            
            db_path = Path(f"{db_name}.db")
            if not os.path.exists(db_path):
                click.echo(f"Error: The database '{db_name}' does not exist.")
                return
            
            with open(db_path, "rb") as db_file:
                db_content = pickle.load(db_file)
            
            for table in tables_data.get('tables', []):
                table_name = table.get('name')
                if table_name in db_content['tables']:
                    click.echo(f"Error: Table '{table_name}' already exists in the database.")
                    continue
                
                db_content['tables'][table_name] = {
                    'columns': table.get('columns', [])
                }
            
            with open(db_path, "wb") as db_file:
                pickle.dump(db_content, db_file)
            
            click.echo(f"Tables created in database '{db_name}'.")
    
    except json.JSONDecodeError as e:
        click.echo(f"Error: Failed to parse JSON file. {e}")
    except Exception as e:
        click.echo(f"Error: {e}")


@cli.command()
def showtables():
    tables_json_path = os.path.join("database", "tables.json")
    
    if not os.path.exists(tables_json_path):
        click.echo(f"Error: The file '{tables_json_path}' does not exist.")
        return
    
    try:
        with open(tables_json_path, "r") as file:
            tables_data = json.load(file)
            if not validate_table_schema(tables_data):
                click.echo("Error: Invalid table schema.")
                return
            
            db_name = tables_data.get('databaseName')
            if not db_name:
                click.echo("Error: 'databaseName' not found in tables.json.")
                return
            
            db_path = Path(f"{db_name}.db")
            if not os.path.exists(db_path):
                click.echo(f"Error: The database '{db_name}' does not exist.")
                return
            
            with open(db_path, "rb") as db_file:
                db_content = pickle.load(db_file)
            
            click.echo(f"Tables in database '{db_name}':")
            for table_name, table_details in db_content['tables'].items():
                click.echo(f"Table: {table_name}")
                for column in table_details['columns']:
                    column_name = column.get('name')
                    column_type = column.get('type')
                    constraints = ', '.join(column.get('constraints', []))
                    click.echo(f"  Column: {column_name}, Type: {column_type}, Constraints: {constraints}")
    
    except json.JSONDecodeError as e:
        click.echo(f"Error: Failed to parse JSON file. {e}")
    except Exception as e:
        click.echo(f"Error: {e}")