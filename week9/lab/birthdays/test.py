from db_manager import BirthdayDbManager

db = BirthdayDbManager("birthdays.db", "birthdays")

# Read data

bdays = db.get_birthdays()

print(bdays)

# Insert data

# db.insert_birthday(name="Naruto", month=10, day=10)
print()
search_res = db.search_birthday_by_name("Naruto")
print(search_res)