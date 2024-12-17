import click
import pickle
import json
import os
from schema.validate import validate_data
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
