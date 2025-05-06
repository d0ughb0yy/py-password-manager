import sqlite3
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
import base64


class UserAccount:
    def __init__(self, acc_name, acc_email, acc_pass, iv):
        self.name = acc_name
        self.email = acc_email
        self.password = acc_pass
        self.iv = iv


master = "masterPasswd"
salt = b'\x19\xb6\x9ec0Xu\x9fghz\x08\xc4\xc4$@]\xd2B\xc9|wk\x1a\xb1\xc9\xbb"1\x1f\x8a\xd3'
key = PBKDF2(master, salt, dkLen=32)
mode = AES.MODE_CBC
cipher = AES.new(key, mode)
iv = cipher.iv


conn = sqlite3.connect("accounts.db")
c = conn.cursor()

# c.execute("""CREATE TABLE accounts (
#             name text,
#             email text,
#             password text,
#             iv text
#             )""")


def encrypt(user_object):
    '''Takes a UserAccount class and encodes the email and password
        and returns a new UserAccount class with the encrypted email and password values'''
    
    # Take the plain-text info and first base64 encoded and turn into bytes
    user_email_b64 = base64.b64encode(user_object.email.encode())
    user_password_b64 = base64.b64encode(user_object.password.encode())

    
    user_email_enc = cipher.encrypt(pad(user_email_b64, AES.block_size))
    user_password_enc = cipher.encrypt(pad(user_password_b64, AES.block_size))
    print(f"Encrypted email: {user_email_enc}")

    return UserAccount(user_object.name, user_email_enc, user_password_enc, iv=iv)


def decrypt(enc_user_object):
    cipher_dec = AES.new(key, mode, enc_user_object.iv)
    user_email_b64 = unpad(cipher_dec.decrypt(enc_user_object.email), AES.block_size)
    user_password_b64 = unpad(cipher_dec.decrypt(enc_user_object.password), AES.block_size)

    print(f"## {enc_user_object.name} ##Email B64: {user_email_b64}, Pass B64: {user_password_b64} ##")

    user_em = base64.b64decode(user_email_b64).decode()
    user_pass = base64.b64decode(user_password_b64).decode()

    return UserAccount(enc_user_object.name, user_em, user_pass, enc_user_object.iv)


account_name_input = input("What is this account for?\n")
account_email_input = input("Enter the email address:\n")
account_password_input = input("Enter password for the account:\n")


user = UserAccount(account_name_input, account_email_input,
                   account_password_input, iv=iv)



# def insert(account_name, account_mail, account_password, iv):
#     connection = sqlite3.connect("accounts.db")
#     db_con = connection.cursor()
#     db_con.execute("INSERT INTO accounts VALUES(?, ?, ?, ?)",
#                    (account_name, account_mail, account_password, iv))
#     connection.commit()
#     connection.close()





encrypted_user_info = encrypt(user)
decrypted_user_info = decrypt(encrypted_user_info)

print(f"""For the account: {decrypted_user_info.name}:
      Email: {decrypted_user_info.email}
      Password: {decrypted_user_info.password}
      """)