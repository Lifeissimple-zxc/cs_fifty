import sqlite3
from atexit import register

class BirthdayDbManager:
    """
    Helper for interacting with local sqlite database
    """
    def __init__(self, db_path: str, table: str):
        """
        Instantiates our class, stores sqlite3 conn and cursor objects within self
        """
        self.db_conn = sqlite3.connect(db_path, check_same_thread=False)
        # Make our rows dict-like
        self.db_conn.row_factory = sqlite3.Row

        self.cursor = self.db_conn.cursor()
        self.table = table

        # close conn  automatically on exit
        register(self.db_conn.close)


    def get_birthdays(self) -> list:
        """
        Gets data on ALL birthdays from the table
        """
        self.cursor.execute("SELECT name, month, day FROM birthdays")
        rows = self.cursor.fetchall()
        # Convert to a list of dicts
        data = [dict(row) for row in rows]
        return data


    def insert_birthday(self, **kwargs) -> None:
        """
        Inserts a row the birthdays table
        """
        # Parse data to insert
        cols, vals = list(kwargs.keys()), list(kwargs.values())
        cols = ", ".join(cols)
        vals_placeholder = ", ".join(["?" for entry in vals])
        # Prepare SQL statement
        stmt = f"INSERT INTO birthdays ({cols}) VALUES ({vals_placeholder})"
        # Execute statement
        try:
            self.cursor.execute(stmt, vals)
            self.db_conn.commit()
        except Exception as e:
            print(f"Caught error: {str(e)}")


    def search_birthday_by_name(self, name) -> list:
        """
        Performs a search for birhtdays by name
        """
        self.cursor.execute("SELECT name, month, day FROM birthdays WHERE LOWER(name) = ?", (name.lower(),))
        rows = self.cursor.fetchall()
        # Convert to a list of dicts
        data = [dict(row) for row in rows]
        return data

