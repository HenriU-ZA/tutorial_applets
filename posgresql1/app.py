from posgresql1.user import User
from posgresql1.database import Database

Database.initialise(database="learning", host="localhost", user="postgres", password="1234")

my_user = User('pieter@goodemole.com', 'Pieter', 'Arendse', None)
my_user.save_to_db()

user_from_db = User.load_from_db_by_email('mail@jungle.com')

print(user_from_db)
