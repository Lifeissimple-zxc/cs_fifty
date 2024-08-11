from finance_tools.db_manager import DbManager
import json

# Read constants from JSON
with open("static/const.json") as file:
    CONSTANTS = json.loads(file.read())
# Storing nested data to variables for convenience
DB_TABLES = CONSTANTS["DB_TABLES"]
# Useful classes to shorten import lines in higher level scrpts
