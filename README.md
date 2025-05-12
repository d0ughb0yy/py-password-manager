# pyPasswordManager
### Description
Password manager written in python that encrypts and stores account credentials using AES
encryption and SQLite for local storage.
### Features
* Encryption of email and password data using pycryptodome library
* SQLite database for storing account names, usernames and encrypted passwords
* CRUD operations (Create, Read, Update, Delete) for managing credentials
### Libraries used
* pycryptodome
* sqlite3
* base64
* os
* argparse
* dotenv
## Usage
Add an entry to the database:\
`python3 pypass.py -f add -n Google -u test@gmail.com -p password123`\

Query for account names:\
`python3 pypass.py -f view -n Google`
## Details
