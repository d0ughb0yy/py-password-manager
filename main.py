import sys
import argparse

from crypto import encrypt, decrypt

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--account", help="Name of the account")
parser.add_argument("-u", "--username", help="Username used in the account")
parser.add_argument("-p", "--password", help="Password for the account")
args = parser.parse_args()

user_accounts = {}

# Get account information from the command line arguments
acc_name_input = args.account
acc_username_input = args.username
acc_pass_input = args.password

# Add the account information into a dictionary
user_accounts[acc_name_input] = [acc_username_input, acc_pass_input]

print(encrypt(user_accounts, acc_name_input))
print(decrypt(user_accounts, acc_name_input))