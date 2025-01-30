from orm import BaseModel 

# Define a model
class User(BaseModel):
    _database_name = "MyFirstDB"  # From main.json
    _table_name = "users"         # From tables.json

# Insert data
user = User(name="Alice", email="alice@example.com")
user.save()

# Query data
print(User.objects())