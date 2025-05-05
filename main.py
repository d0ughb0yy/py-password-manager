import argparse

from crypto import encrypt, decrypt

user_accounts = {}

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--function", help="Function to perform add or view", required=True)
parser.add_argument("-n", "--name", help="Name of the account", required=True)
parser.add_argument("-u", "--username", help="Username used in the account")
parser.add_argument("-p", "--password", help="Password for the account")
args = parser.parse_args()

# Get account information from the command line arguments
acc_name_input = args.name
acc_username_input = args.username
acc_pass_input = args.password

# Assign user input to the user dictionary
user_accounts[acc_name_input] = [acc_username_input, acc_pass_input]

# Application logic for --function argument
if args.function == "view":
    try:
        print(decrypt(acc_name_input))
    except Exception as e:
        print(f"Error during decryption: {e}")
elif args.function == "add":
    encrypt(user_accounts, acc_name_input)