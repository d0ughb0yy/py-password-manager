import sqlite3
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
import base64
import os
from dotenv import load_dotenv

# Load Environmental Variables
load_dotenv()

SALT = os.getenv("SALT")
MASTER = os.getenv("MASTER_PASS")

key = PBKDF2(MASTER, SALT, dkLen=32)
mode = AES.MODE_CBC


class UserAccount:
    def __init__(self, acc_name, acc_email, acc_pass, iv):
        self.name = acc_name
        self.email = acc_email
        self.password = acc_pass
        self.iv = iv

cipher = AES.new(key, mode)
iv = cipher.iv


def check_for_db():
    '''Checks for presence of accounts.db file in the working directory,
        if the file is not present it creates it and initializes columns'''
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


def encrypt(user_object):
    """Takes a UserAccount class and encodes the email and password
        and returns a new UserAccount class with the encrypted email and password values"""

    # Take the plain-text info and first base64 encode it and turn into bytes
    user_email_b64 = base64.b64encode(user_object.email.encode())
    user_password_b64 = base64.b64encode(user_object.password.encode())

    # Encrypt the base64 encoded email and password
    user_email_enc = cipher.encrypt(pad(user_email_b64, AES.block_size))
    user_password_enc = cipher.encrypt(pad(user_password_b64, AES.block_size))
    print(f"Encrypted email: {user_email_enc}, Encrypted Pass: {user_password_enc}")

    # Populates a new UserAccount object with encrypted values
    return UserAccount(user_object.name, user_email_enc, user_password_enc, iv=iv)


def decrypt(enc_user_object):
    """Takes an UserAccount object populated with encrypted email and password,
        It then decrypts them and returns in another UserAccount object"""

    # Declare a new cipher for decrypting with the iv from the database
    cipher_dec = AES.new(key, mode, enc_user_object.iv)

    # Unpads and decrypts into base64 encoding
    user_email_b64 = unpad(cipher_dec.decrypt(
        enc_user_object.email), AES.block_size)
    user_password_b64 = unpad(cipher_dec.decrypt(
        enc_user_object.password), AES.block_size)

    # Decode from base64 and decode from bytes
    user_em = base64.b64decode(user_email_b64).decode()
    user_pass = base64.b64decode(user_password_b64).decode()

    # Return a UserAccount object populated with decrypted account info
    return UserAccount(enc_user_object.name, user_em, user_pass, enc_user_object.iv)

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
        for tuple in db_dump:
            user_tuple = tuple
            # Extracts the values from every tuple to and stores them into a UserAccount class
            encrypted_user = UserAccount(user_tuple[0], user_tuple[1], user_tuple[2], user_tuple[3])
            decrypted_user = decrypt(encrypted_user)
            view_conn.close()
            print(f"""Account: {decrypted_user.name}\nEmail: {decrypted_user.email}\nPassword: {decrypted_user.password}""")
            print("=========================")
    else:
        print("Accounts file is missing.")
        print("Add an entry with --add first")
