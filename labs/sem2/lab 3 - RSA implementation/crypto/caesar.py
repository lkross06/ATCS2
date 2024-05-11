import random

class Caesar:
    '''
    creates a new caesar cipher object
    
    :param keys: the JSON-encoded password. if not specified, password is randomly generated
    '''
    def __init__(self, keys:dict[str,int] = None):
        self.__printable = [x for x in range(32, 126 + 1)] #all printable characters
        
        if keys == None or keys.get("password") == None:
            self.__password = random.randint(1, 999) #arbitrary auto-generated password
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
    performs a caesar encryption

    :param message: the plaintext to process

    :return: ciphertext after cipher
    '''
    def encrypt(self, message:str) -> str:
        ciphertext = ""

        for i in message:
            if ord(i) in self.__printable:
                '''
                1. add ascii table index to password (shift)
                2. subtract 95 to account for looping from end-->start
                3. mod 26 to get actual displacement from 95
                4. add index of 95 back for actual self.__printable answer

                this works because (-n) % 95 = 95 - n so it handles loops
                '''
                ciphertext += chr((ord(i) + self.__password - self.__printable[0]) % len(self.__printable) + self.__printable[0])
            else:
                return "Error: INVALID CHARACTER: ASCII " + ord(i)
        
        return ciphertext

    '''
    performs a caesar decryption

    :param message: the ciphertext to process

    :return: plaintext
    '''
    def decrypt(self, message:str) -> str:

        plaintext = ""

        for i in message:
            if ord(i) in self.__printable:
                '''
                1. subtract ascii table index and password (shift back)
                2. subtract 95 to account for looping from end-->start
                3. mod 26 to get actual displacement from 95
                4. add index of 95 back for actual printable answer

                this works because (-n) % 95 = 95 - n so it handles loops
                '''
                plaintext += chr((ord(i) - self.__password - self.__printable[0]) % len(self.__printable) + self.__printable[0])
            else:
                return "Error: INVALID CHARACTER: ASCII " + ord(i)
        

        return plaintext
    
    '''
    JSON-encodes password for ease of transferring

    :return: a JSON with the password
    '''
    def encode_keys(self) -> dict[str,int]:
        return {"password": self.__password}