import base64
from pyexpat.errors import messages

from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import pickle
import os

master = 'masterPasswd'
salt = b'\x19\xb6\x9ec0Xu\x9fghz\x08\xc4\xc4$@]\xd2B\xc9|wk\x1a\xb1\xc9\xbb"1\x1f\x8a\xd3'

key = PBKDF2(master, salt, dkLen=32)
mode = AES.MODE_CBC

def load_encrypted_accounts(acc_name_input):
    """Load existing encrypted accounts from file"""
    if not os.path.exists(acc_name_input + ".txt"):
        print("No existing accounts file found.")
        return {}

    try:
        with open(acc_name_input + ".txt", "rb") as storage:
            pickled_data = storage.read()
            if not pickled_data:  # Empty file
                return {}
            return pickle.loads(pickled_data)
    except (pickle.UnpicklingError, EOFError) as e:
        print(f"Error loading accounts file: {e}")
        return {}

def save_encrypted_accounts(encrypted_accounts, acc_name_input):
    """Save the complete accounts dictionary to file"""
    pickled_data = pickle.dumps(encrypted_accounts)
    with open(acc_name_input + ".txt", "wb") as storage:
        storage.write(pickled_data)


def encrypt(user_accounts, acc_name_input):
    # Check if the account exists
    if acc_name_input not in user_accounts:
        print(f"Account '{acc_name_input}' not found in user accounts.")
        return False
    # Load existing encrypted accounts if the file exists
    # encrypted_accounts = load_encrypted_accounts(acc_name_input)
    cipher = AES.new(key, mode)
    iv = cipher.iv

    # Base64 encode the mail and password separately and turn them into bytes
    account_mail_b64 = base64.b64encode(user_accounts[acc_name_input][0].encode())
    account_pass_b64 = base64.b64encode(user_accounts[acc_name_input][1].encode())

    # Initialize the encrypted accounts dictionary
    encrypted_accounts = {}
    encrypted_email = cipher.encrypt(pad(account_mail_b64, AES.block_size)) # Encrypt the base64 email
    encrypted_pass = cipher.encrypt(pad(account_pass_b64, AES.block_size)) # Encrypt the base64 password

    # Store the values into a dictionary
    encrypted_accounts[acc_name_input] = [encrypted_email, encrypted_pass, iv]

    # Serialize the dictionary using pickle
    save_encrypted_accounts(encrypted_accounts, acc_name_input)

    print(f"Account {acc_name_input} encrypted and saved!")
    return True


def decrypt(acc_name_input):
    try:
        # Load the encrypted accounts dictionary
        encrypted_accounts = load_encrypted_accounts(acc_name_input)

        if acc_name_input not in encrypted_accounts:
            print(f"Account '{acc_name_input}' not found in encrypted accounts")
            return None
        encrypted_email, encrypted_pass, iv = encrypted_accounts[acc_name_input]

        # Create cipher with the IV
        cipher = AES.new(key, mode, iv=iv)

        # Decrypt and unpad
        decrypted_email_b64 = unpad(cipher.decrypt(encrypted_email), AES.block_size)
        decrypted_pass_b64 = unpad(cipher.decrypt(encrypted_pass), AES.block_size)

        # Decode from b64
        email = base64.b64decode(decrypted_email_b64).decode()
        password = base64.b64decode(decrypted_pass_b64).decode()

        message = (f"Account: {acc_name_input}\n"
                   f"Email: {email}\n"
                   f"Password: {password}")

        return message

    except Exception as e:
        print(f"Error decrypting account: {e}")
        return None