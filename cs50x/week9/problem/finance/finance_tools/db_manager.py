import sqlite3
from atexit import register


class DbManager:
    """
    Helper for interacting with local sqlite database
    """

    def __init__(self, db_path: str):
        """
        Instantiates our class, stores sqlite3 conn and cursor objects within self
        """
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        # Make our rows dict-like
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        # Close conn  automatically on exit
        register(self.conn.close)

    def rows_to_dict(self):
        """
        Fetches rows from cursor after the query has been executed
        """
        data = self.cursor.fetchall()
        # TODO: make it an iter?
        data = [dict(row) for row in data]
        return data

    def register_new_user(self, username: str, hashed_password: str):
        """
        Inserts a new user record to users table
        """
        statement = "INSERT INTO users (username, hash) VALUES (?, ?)"
        try:
            self.cursor.execute(statement, (username, hashed_password))
            self.conn.commit()
        except Exception as e:
            # The below should be a logger call in the ideal world
            print(f"DB caught an error when adding a new user: {str(e)}")

    # TODO make it more abstracted, put pasring of input data to a separate func
    def update_user_balance(self, user_id: int, new_balance: float):
        """
        Update user_id balance to new_balance
        """
        stmt = f"UPDATE users SET cash = ? WHERE id = ?"
        try:
            self.cursor.execute(stmt, (new_balance, user_id))
            self.conn.commit()
        except Exception as e:
            # The below should be a logger call in the ideal world
            print(f"DB caught an error when updating balance for {user_id}: {str(e)}")

    # TODO this can be abstracted better
    def increment_user_balance(self, user_id: int, increment: float):
        """
        Update user_id balance to new_balance
        """
        stmt = """
            UPDATE users
            SET cash = cash + ?
            WHERE id = ?
        """
        try:
            self.cursor.execute(stmt, (increment, user_id))
            self.conn.commit()
        except Exception as e:
            # The below should be a logger call in the ideal world
            print(f"DB caught an error when updating balance for {user_id}: {str(e)}")

    def get_data(self, table: str, cols_needed: list = None, **kwargs):
        """
        Reads users' data(username, hash) to a list of dicts with kwargs used for filtering data
        """
        if cols_needed is None:
            cols_needed = []
        filter_cols, filter_vals = list(kwargs.keys()), list(kwargs.values())
        # Conditional assigment of cols needed to query
        col_list_str = ", ".join(cols_needed) if len(cols_needed) > 0 else "*"
        vals_placeholder = ", ".join(["?" for entry in filter_vals])
        # Prepare statement
        # Base select
        stmt = f"SELECT {col_list_str} FROM {table} WHERE TRUE"
        # Adding filters
        filters = [f"{key} = ?" for key in filter_cols]
        if len(filters) == 1:
            filters = f" AND {filters[0]}"
        else:
            filters = " AND".join(filters)
        stmt += filters
        # Execute SQL
        try:
            self.cursor.execute(stmt, filter_vals)
        except Exception as e:
            print(f"DB caught an error when getting data with {kwargs} filters: {str(e)}")
            raise e
        data = self.rows_to_dict()
        return data

    def insert_row(self, table: str, row_data: dict):
        """
        Unpacks data into column: value form and inserts it to the table as 1 row
        """
        cols, vals = list(row_data.keys()), list(row_data.values())
        cols_str = ", ".join(cols)
        vals_placeholder = ", ".join("?" for entry in vals)
        # Prepare statement
        stmt = f"INSERT INTO {table}({cols_str}) VALUES ({vals_placeholder})"
        # Execute
        try:
            self.cursor.execute(stmt, vals)
            self.conn.commit()
        except Exception as e:
            print(f"Got errors when inserting {row_data} to {table}: {e}")

    def get_transactions_summary(self, user_id: int) -> list:
        """
        Runs a query to get all-time stats of an account with user_id
        """
        stmt = """
            SELECT
                symbol                                                              AS stock,
                (SUM(CASE WHEN transaction_type = 1 THEN shares ELSE 0 END)
                 - SUM(CASE WHEN transaction_type = 2 THEN shares ELSE 0 END))      AS shares
            FROM transactions
            WHERE TRUE
                AND user_id = ?
            GROUP BY 1
            HAVING (SUM(CASE WHEN transaction_type = 1 THEN shares ELSE 0 END)
                 - SUM(CASE WHEN transaction_type = 2 THEN shares ELSE 0 END)) > 0
            ORDER BY 1 ASC
        """
        self.cursor.execute(stmt, (user_id,))
        return self.rows_to_dict()

    def get_stock_balance(self, user_id: int, symbol: str) -> list:
        """
        Runs a query to get symbol shares of a user_ud
        """
        stmt = """
            SELECT
                symbol                                                              AS stock,
                (SUM(CASE WHEN transaction_type = 1 THEN shares ELSE 0 END)
                 - SUM(CASE WHEN transaction_type = 2 THEN shares ELSE 0 END))      AS shares
            FROM transactions
            WHERE TRUE
                AND user_id = ?
                AND symbol = ?
            GROUP BY 1
        """
        self.cursor.execute(stmt, (user_id, symbol,))
        return self.rows_to_dict()

    def fetch_history(self, start_utc: int, end_utc: int,
                      user_id: int, symbol: str = None) -> list:
        """
        Fetches data on transactions where 1 row represents a single transaction
        """
        stmt = """
            SELECT
                DATETIME(
                    transaction_ts / 1000, 'unixepoch'
                )                                                       AS transaction_ts,
                symbol                                                  AS stock,
                CASE
                    WHEN transaction_type = 1 THEN shares
                    WHEN transaction_type = 3 THEN shares
                    WHEN transaction_type = 2 THEN  -1 * (shares)
                END                                                     AS shares,
                total_price                                             AS total_price
            FROM transactions
            WHERE TRUE
                AND transaction_ts >= ?
                AND transaction_ts < ?
                AND user_id = ?
                AND symbol = ?
            ORDER BY transaction_ts DESC
        """
        if symbol is None:
            stmt = stmt.replace("AND symbol = ?", "")
            self.cursor.execute(stmt, (start_utc, end_utc, user_id,))
        else:
            self.cursor.execute(stmt, (start_utc, end_utc, user_id, symbol,))
        print(stmt, start_utc, end_utc, user_id, symbol)
        return self.rows_to_dict()

