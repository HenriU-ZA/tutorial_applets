from posgresql1.user import User

my_user = User('sara@grouwer.com', 'Sara', 'grouwer', None)
my_user.save_to_db()

user_from_db = User.load_from_db_by_email('mail@jungle.com')

print (user_from_db)

