from week9.problem.finance.finance_tools.db_manager import DbManager

USER = 1

db = DbManager("finance.db")

data = db.get_data(cols_needed=["id", "cash"],
                   table="users", id=USER)

print(f"Pre change: {data}")
print(data)
new_balance = data[0]["cash"] + 100

db.update_user_balance(user_id=USER, new_balance=new_balance)

data = db.get_data(cols_needed=["id", "cash"], table="users", id=USER)
print(f"Post change: {data}")
