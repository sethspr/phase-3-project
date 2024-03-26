from __init__ import CURSOR, CONN
from username import Username
from password import Password
import random
import string


class User:
    all = {}
    def __init__ (self, first_name, last_name, id = None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name 

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of User instances """
        sql = """
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists User  instances """
        sql = """
            DROP TABLE IF EXISTS users;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Insert a new row with the first_name and last_name values of the current User object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key."""
        sql = """
                INSERT INTO users (first_name, last_name)
                VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.first_name, self.last_name))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

        # Create a username for the user
        Username.create_table()
        username = Username.create(username=self.generate_username(), user_id=self.id)
        return username
        
    def generate_username(self):
        """Generate a username based on the user's first name and last name"""
        # Implement your username generation logic here
        # For example, concatenate first name and last name
        new_user_name = self.first_name[0].upper() + self.last_name.lower()
        random_numbers = ''.join(random.choices(string.digits, k=2))
        new_user_name += random_numbers
        return new_user_name


    @classmethod
    def create(cls, first_name, last_name):
        """ Initialize a new User instance and save the object to the database. Return the new instance. """
        user = cls(first_name, last_name,)
        user.save()


    @classmethod
    def instance_from_db(cls, row):
        """Return an User instance having the attribute values from the table row."""
        # Check the dictionary for  existing instance using the row's primary key
        user = cls.all.get(row[0])
        if user:
            # ensure attributes match row values in case local instance was modified
            user.first_name = row[1]
            user.last_name = row[2]
        # not in dictionary, create new instance and add to dictionary
        else:
            user = cls(row[1], row[2])
            user.id = row[0]
            cls.all[user.id] = user
        return user

    @classmethod
    def find_by_id(cls, id):
        """Return a User instance having the attribute values from the table row."""
        sql = """
            SELECT *
            FROM users
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def update(self):
        """Update the table row corresponding to the current User instance."""
        sql = """
            UPDATE users
            SET first_name = ?, last_name = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.first_name, self.last_name,
                            self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current User instance,
        delete the dictionary entry, and reassign id attribute"""
        sql = """
            DELETE FROM users
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        
        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def get_all(cls):
        """Return a list containing one Review instance per table row"""
        sql = """
            SELECT *
            FROM users
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]  

    @classmethod
    def user_list(cls):
        for user_id in cls.all:
            user = cls.all[user_id]
            if user.id is not None:
                username = Username.find_by_id(user_id)
                password = Password.find_by_id(username_id = user_id)
                if username:
                    print(f"User Id: {user.id} User Info: {user.first_name} {user.last_name} Username: {username.username} Password: {password.password}")
                else:
                    print(f"User Id: {user.id} User Info: {user.first_name} {user.last_name} (No username found)")


if __name__ == '__main__':
    User.create_table()



    # john = User.create(first_name= 'John', last_name= 'Smith')
    # emily = User.create(first_name = 'Emily', last_name = 'Johnson')
    # michael = User.create(first_name = 'Michael' , last_name ='Williams')
    # sarah = User.create(first_name = 'Sarah', last_name = 'Jones')
    # christopher = User.create(first_name = 'Christopher', last_name = 'Brown')
    # jessica = User.create(first_name = 'Jessica', last_name = 'Davis')
    # matthew = User.create(first_name = 'Matthew', last_name = 'Miller')
    # amanda = User.create(first_name = 'Amanda', last_name = 'Wilson')
    # david = User.create(first_name = 'David', last_name = 'Moore')
    # jennifer = User.create(first_name = 'Jennifer', last_name = 'Taylor')
    # jc = User.create(first_name= 'John', last_name= 'Cena')
    # brad = User.create(first_name= 'Brad', last_name= 'Pitt')

    # User.user_list()
    # User.drop_table()
    # Username.drop_table()
    # Password.drop_table()

