import random

class Vigenere:
    '''
    creates a new vigenere cipher object
    
    :param keys: the JSON-encoded password. if not specified, password is randomly generated
    '''
    def __init__(self, keys:dict[str,int] = None):
        self.__printable = [x for x in range(32, 126 + 1)] #all printable characters

        if keys == None or keys.get("password") == None:
            #arbitrary auto-generated password of random printable characters that is 1-999 characters long
            self.__password = "".join([chr(x) for x in [random.randint(32, 126) for n in range(random.randint(1, 999))]])
        else:
            self.__password = keys["password"]

    '''
    reads the file specific to the type of expected file data

    :param i: the input file path
    :param mode: the mode (expecting "encrypt" or "decrypt")

    :return: correctly parsed input data, None if not found
    '''
    def read_file(self, i:str, mode:str):
        try:
            if mode == "encrypt" or mode == "decrypt":
                with open(i, "r") as file:
                    return "".join([str(x).removesuffix("\n") for x in file.readlines()])

            return None
        except:
            return None

    '''
    gets repeating vigenere password based on plaintext/ciphertext
    ex: "hello", "hi" --> "hihih"

    :param message: the plaintext/ciphertext in the cipher

    :return: repeating password
    '''
    def __get_vigenere_password(self, message:str) -> str:
        pi = 0
        password = [x for x in str(self.__password).lower()] #convert to list to point to each individual char
        rtn = ""

        for i in message:
            rtn += password[pi % len(password)] #modulo of length n loops from n --> 0
            pi += 1
        return rtn

    '''
    performs a vigenere encryption

    :param message: the plaintext to process

    :return: ciphertext
    '''
    def encrypt(self, message:str) -> str:

        pwd = self.__get_vigenere_password(message)
        ciphertext = ""

        for i in range(len(message)):
            if ord(message[i]) in self.__printable:
                '''
                1. add password index to starting index to shift
                2. subtract by first printable character index
                3. mod by 95 to get 0-95 position
                4. add back to convert from non-printable to printable characters
                '''
                ciphertext += chr(((ord(message[i]) + ord(pwd[i]) - self.__printable[0]) % len(self.__printable)) + self.__printable[0])
            else:
                return "Error: INVALID CHARACTER: ASCII " + ord(i)
        
        return ciphertext

    '''
    performs a vigenere decryption

    :param message: the ciphertext to process

    :return: a JSON with the status and plaintext of the cipher
    '''
    def decrypt(self, message:str) -> str:
        pwd = self.__get_vigenere_password(message)
        plaintext = ""

        for i in range(len(message)):
            if ord(message[i]) in self.__printable:
                '''
                1. subtract password index by starting index to shift
                2. subtract by first printable character index
                3. mod by 95 to get 0-95 position
                4. add back to convert from non-printable to printable characters
                '''
                plaintext += chr(((ord(message[i]) - ord(pwd[i]) - self.__printable[0]) % len(self.__printable)) + self.__printable[0])
            else:
                return "Error: INVALID CHARACTER: ASCII " + ord(i)
            
        return plaintext
    
    '''
    JSON-encodes password for ease of transferring

    :return: a JSON with the password
    '''
    def encode_keys(self) -> dict[str,int]:
        return {"password": self.__password}