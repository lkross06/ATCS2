printable = [x for x in range(32, 126 + 1)] #all printable characters

'''
removes \ for string formatting with double quotations ""

@param message(string): message to encrypt/decrypt

@return (array): message as array of strings with \ removed
'''
def remove_backslashes(message):
    message = [x for x in message]
    for i in message:
        if i == '\\':
            message.remove(i)
            
    return message
'''
processes form data and calls necessary cipher

@param cipher(string): caesar or vigenere
@param mode(string): encrypt or decrypt
@param message(string): the plaintext/ciphertext to process
@param password(string): the password for the cipher

@return (json): a JSON with the status and message of the cryptography 
'''
def get_symmetric(cipher, mode, message, password):
    message = remove_backslashes(message)

    if cipher == "caesar":
        if mode == "encrypt":
            return caesar_encrypt(message, password)
        elif mode == "decrypt":
            return caesar_decrypt(message, password)
    elif cipher == "vigenere":
        if mode == "encrypt":
            return vigenere_encrypt(message, password)
        elif mode == "decrypt":
            return vigenere_decrypt(message, password)

    return {"status":"error", "message":"INVALID INPUTS"}

'''
performs a caesar encryption

@param message(string): the plaintext to process
@param password(string): the password for the cipher

@return (json): a JSON with the status and ciphertext of the cipher
'''
def caesar_encrypt(message, password):
    if not(str(password).isnumeric()):
        return {"status":"error", "message":"INVALID PASSWORD"}
    
    password = int(password)

    ciphertext = ""

    for i in message:
        if ord(i) in printable:
            '''
            1. add ascii table index to password (shift)
            2. subtract 95 to account for looping from end-->start
            3. mod 26 to get actual displacement from 95
            4. add index of 95 back for actual printable answer

            this works because (-n) % 95 = 95 - n so it handles loops
            '''
            ciphertext += chr((ord(i) + password - printable[0]) % len(printable) + printable[0])
        else:
            print(i)
            return {"status":"error", "message":"INVALID CHARACTER: ASCII " + ord(i)}
    

    return {"status":"encrypt", "message":ciphertext}

'''
performs a caesar decryption

@param message(string): the ciphertext to process
@param password(string): the password for the cipher

@return (json): a JSON with the status and plaintext of the cipher
'''
def caesar_decrypt(message, password):
    if not(str(password).isnumeric()):
        return {"status":"error", "message":"INVALID PASSWORD"}
    
    password = int(password)

    plaintext = ""

    for i in message:
        if ord(i) in printable:
            '''
            1. subtract ascii table index and password (shift back)
            2. subtract 95 to account for looping from end-->start
            3. mod 26 to get actual displacement from 95
            4. add index of 95 back for actual printable answer

            this works because (-n) % 95 = 95 - n so it handles loops
            '''
            plaintext += chr((ord(i) - password - printable[0]) % len(printable) + printable[0])
        else:
            return {"status":"error", "message":"INVALID CHARACTER: ASCII " + ord(i)}
    

    return {"status":"decrypt", "message":plaintext}

'''
gets repeating vigenere password based on plaintext/ciphertext
ex: "hello", "hi" --> "hihih"

@param message(string): the plaintext/cipherttext in the cipher
@param password(string): the password for the cipher

@return (string): repeating password
'''
def get_vigenere_password(message, password):
    pi = 0
    password = [x for x in str(password).lower()] #convert to list to point to each individual char
    rtn = ""

    for i in message:
        rtn += password[pi % len(password)] #modulo of length n loops from n --> 0
        pi += 1
    return rtn

'''
performs a vigenere encryption

@param message(string): the plaintext to process
@param password(string): the password for the cipher

@return (json): a JSON with the status and ciphertext of the cipher
'''
def vigenere_encrypt(message, password):
    if not(len(password) > 0):
        return {"status":"error", "message":"INVALID PASSWORD"}

    pwd = get_vigenere_password(message, password)
    ciphertext = ""

    for i in range(len(message)):
        if ord(message[i]) in printable:
            '''
            1. add password index to starting index to shift
            2. subtract by first printable character index
            3. mod by 95 to get 0-95 position
            4. add back to convert from non-printable to printable characters
            '''
            ciphertext += chr(((ord(message[i]) + ord(pwd[i]) - printable[0]) % len(printable)) + printable[0])
        else:
            return {"status":"error", "message":"INVALID CHARACTER: ASCII " + ord(i)}
    print(ciphertext) 
    return {"status":"encrypt", "message":ciphertext}

'''
performs a vigenere decryption

@param message(string): the ciphertext to process
@param password(string): the password for the cipher

@return (json): a JSON with the status and plaintext of the cipher
'''
def vigenere_decrypt(message, password):
    if not(len(password) > 0):
        return {"status":"error", "message":"INVALID PASSWORD"}

    pwd = get_vigenere_password(message, password)
    plaintext = ""

    for i in range(len(message)):
        if ord(message[i]) in printable:
            '''
            1. subtract password index by starting index to shift
            2. subtract by first printable character index
            3. mod by 95 to get 0-95 position
            4. add back to convert from non-printable to printable characters
            '''
            plaintext += chr(((ord(message[i]) - ord(pwd[i]) - printable[0]) % len(printable)) + printable[0])
        else:
            return {"status":"error", "message":"INVALID CHARACTER: ASCII " + ord(i)}
        
    return {"status":"decrypt", "message":plaintext}