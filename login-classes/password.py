from __init__ import CURSOR, CONN
from password import Username

class Password:
    all = {}
    def __init__ (self, username_id, password, id = None):
        self.id = id
        self.password = password
        self.username_id = username_id

    def __repr__(self):
        return (
            f"<Password {self.id}: {self.password}, " +
            f"User ID: {self.username_id}>"
        )

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        if isinstance(password, str) and 0 < len(password) <= 3:
            self._password = password
        else:
            raise ValueError(
                "Password must be a non-empty string less than or equal to 3 characters"
            )

    @property
    def username_id(self):
        return self._username_id

    @username_id.setter
    def username_id(self, username_id):
        if type(username_id) is int and Username.find_by_id(username_id):
            self._username_id = username_id
        else:
            raise ValueError(
                "user_id must reference a user in the database")

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Password instances """
        sql = """
            CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            password TEXT,
            username_id INTEGER,
            FOREIGN KEY (username_id) REFERENCES usernames(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Password instances """
        sql = """
            DROP TABLE IF EXISTS passwords;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the password and username_id values of the current Password object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO passwords (password, username_id)
                VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.password, self.username_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        """Update the table row corresponding to the current password instance."""
        sql = """
            UPDATE passwords
            SET password = ?, username_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.password, self.username_id, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Password instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM passwords
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def create(cls, password, username_id):
        """ Initialize a new password instance and save the object to the database """
        password = cls(password, username_id)
        password.save()
        return password

    @classmethod
    def instance_from_db(cls, row):
        """Return an Username object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        password = cls.all.get(row[0])
        if password:
            # ensure attributes match row values in case local instance was modified
            password.password = row[1]
            password.username_id = row[2]
        else:
            # not in dictionary, create new instance and add to dictionary
            password = cls(row[1], row[2], row[3])
            password.id = row[0]
            cls.all[password.id] = password
        return password
    
    @classmethod
    def get_all(cls):
        """Return a list containing one Password object per table row"""
        sql = """
            SELECT *
            FROM passwords
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        """Return Username object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM passwords
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, password):
        """Return Password object corresponding to first table row matching specified password"""
        sql = """
            SELECT *
            FROM passwords
            WHERE password is ?
        """

        row = CURSOR.execute(sql, (username,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def username(self):
        """Return username associated with current password"""
        sql = """
            SELECT * FROM usernames
            WHERE user_id = ?
        """
        CURSOR.execute(sql, (self.username_id,),)

        rows = CURSOR.fetchall()
        return User.instance_from_db(row)

Password.create_table()