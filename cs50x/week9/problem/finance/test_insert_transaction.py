from week9.problem.finance.finance_tools.db_manager import DbManager

DUMMY_TRANSACTION = {
    "transaction_ts": 1682723775111,
    "user_id": 1,
    "transaction_type": 1,
    "symbol": "testtesttest",
    "shares": 0,
    "total_price": 0
}
db = DbManager("finance.db")


db.insert_row("transactions", DUMMY_TRANSACTION)
