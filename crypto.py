import rsa

publicKey, privateKey = rsa.newkeys(512)

def encrypt(user_accounts, acc_name_input):
    encoded_list = str(user_accounts[acc_name_input])
    encryption = rsa.encrypt(encoded_list.encode(), publicKey)
    user_accounts[acc_name_input] = encryption
    return user_accounts

def decrypt(user_accounts, acc_name_input):
    if acc_name_input in user_accounts:
        decoded_list = user_accounts[acc_name_input] # Takes the list value of an account name from the user_accounts dictionary
        decryption = rsa.decrypt(decoded_list, privateKey).decode() # Decrypts using the privateKey into bytes and then decodes to string
        return decryption
    else:
        return "This account is not registered."