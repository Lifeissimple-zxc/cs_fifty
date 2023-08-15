from finance_tools.db_manager import DbManager

db = DbManager("finance.db")

data = db.get_data(cols_needed=["id", "cash"],
                   table="users", id=1)

print(data)
