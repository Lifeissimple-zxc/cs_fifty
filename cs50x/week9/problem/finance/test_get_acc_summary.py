from finance_tools import DbManager

db = DbManager("finance.db")

acc_summary = db.get_transactions_summary(user_id=1)

print(acc_summary)
