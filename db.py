import sqlite3
import os

from crypto import decrypt, UserAccount

def check_for_db():
    """Checks for presence of accounts.db file in the working directory,
        if the file is not present it creates it and initializes columns"""
    if os.path.exists("accounts.db"):
        pass
    else:
        conn = sqlite3.connect("accounts.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE accounts (
                    name text,
                    email text,
                    password text,
                    iv text
                    )""")
        conn.commit()

def insert_into_db(enc_user_object):
        # Create an accounts.db file if it's not created and initialize the accounts table inside
        check_for_db()
        connection = sqlite3.connect("accounts.db")
        db_con = connection.cursor()
        db_con.execute("INSERT INTO accounts VALUES(?, ?, ?, ?)",
                       (enc_user_object.name, enc_user_object.email, enc_user_object.password, enc_user_object.iv))
        connection.commit()
        connection.close()

def view_entry(acc_name_input):

    if os.path.exists("accounts.db"):
        # Connect
        view_conn = sqlite3.connect("accounts.db")
        vc = view_conn.cursor()

        # Execute SELECT statement
        vc.execute("SELECT * FROM accounts WHERE name=?", (acc_name_input,))
        view_conn.commit()

        # Store everything in a db_dump variable
        db_dump = vc.fetchall()
        # Iterate through the list of tuples
        for user_info in db_dump:
            user_tuple = user_info
            # Extracts the values from every tuple and stores them into a UserAccount class
            encrypted_user = UserAccount(user_tuple[0], user_tuple[1], user_tuple[2], user_tuple[3])
            decrypted_user = decrypt(encrypted_user)
            view_conn.close()
            print(f"""Account: {decrypted_user.name}\nEmail: {decrypted_user.email}\nPassword: {decrypted_user.password}""")
            print("=========================")
    else:
        print("Accounts file is missing.")
        print("Add an entry with --add first")
