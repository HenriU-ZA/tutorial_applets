from posgresql1.database import ConnectionFromPool

class User:
    def __init__(self, email, first_name, last_name, id):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.id = id

    def __repr__(self):
        return f"<User {self.email}>"

    def save_to_db(self):
        """This module will save the user to the database"""
        with ConnectionFromPool() as connection:
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO users(email, first_name, last_name) VALUES(%s, %s, %s)',
                               (self.email, self.first_name, self.last_name))

    @classmethod
    def load_from_db_by_email(cls, email):
        """This module loads a user from the database, using the email address."""
        with ConnectionFromPool() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE email=%s',
                                   (email,))
                user_data = cursor.fetchone()
                return cls(email=user_data[1], first_name=user_data[2], last_name=user_data[3], id=user_data[0])
