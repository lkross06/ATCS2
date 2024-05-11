import json

'''
Implementation of a PlayFair cipher. Supports 5x5 and 6x6 playfair squares.
'''
class PlayFair:
    def __init__(self, password:str, size:int = 5):
        self.__pwd = password.lower()
        self.__size = size #size of playfair square (expected to fill in square)

        #set up square
        self.__char_to_row = dict()
        self.__char_to_col = dict()
        self.__pos_to_char = dict()

        sq_letters = []
        lookup_sq_letters = dict()

        sq_range = range(97, 123) #a-z

        if self.__size == 6:
            sq_range = range(97, 123) + range(48, 57) #add 0-9

        for i in sq_range:
            i = chr(i)
            lookup_sq_letters[i] = False

        for i in self.__pwd:
            if not(i in sq_letters):
                sq_letters.append(i)
                lookup_sq_letters[i] = True

        for i in sq_range:
            i = chr(i)
            if lookup_sq_letters[i] != True:
                if self.__size == 5:
                    if i != "j":
                        sq_letters.append(i)
                else:
                    sq_letters.append(i)
        
        for row in range(self.__size):
            for col in range(self.__size):
                letter = sq_letters[(row * 5) + col]

                self.__char_to_row[letter] = row
                self.__char_to_col[letter] = col
                self.__pos_to_char["".join([str(row), str(col)])] = letter

    '''
    performs a playfair encryption
    :param plaintext: the plaintext to encrypt
    :return: byte array of encrypted ciphertext 
    '''
    def encrypt(self, plaintext:str) -> bytes:
        '''
        1. write out password ignoring duplicates
        2. complete square by adding unused letters alphabetically (combine i/j)
        3. divide plaintext into bigrams
        4. insert "X" between duplicates
        5. add "X" to incomplete bigrams
        6. make squares, shift right and down
        7.
        '''

        #check for good input
        if not(type(plaintext) is str):
            print("Error: bad input")
            quit()

        #parse input
        plaintext = plaintext.lower()

        if self.__size == 5:
            plaintext.replace("j", "i")

        ptemp = plaintext
        plaintext = []

        for i in ptemp:
            if i.isalnum():
                plaintext += i

        plaintext = "".join(plaintext)

        #divide plaintext
        plaintext = [p for p in plaintext]

        for i in range(len(plaintext) - 1):
            if plaintext[i] == plaintext[i + 1]:
                plaintext = [plaintext[j] for j in range(i + 1)] + ["x"] + [plaintext[k] for k in range(i + 1, len(plaintext))]

        if len(plaintext) % 2 != 0:
            plaintext += "x"

        final = []    
        
        for i in range(0, len(plaintext), 2):
            #separate into bigrams
            b1 = plaintext[i]
            b2 = plaintext[i + 1]

            #get rows and cols
            r1 = self.__char_to_row.get(b1)
            c1 = self.__char_to_col.get(b1)

            r2 = self.__char_to_row.get(b2)
            c2 = self.__char_to_col.get(b2)

            if (r1 == r2): #same row, shift right
                #if its in the last spot, go to col zero (very left side)
                new_col1 = c1 + 1 if c1 + 1 < self.__size else 0
                final.append(self.__pos_to_char.get("".join([str(r1), str(new_col1)])))

                new_col2 = c2 + 1 if c2 + 1 < self.__size else 0
                final.append(self.__pos_to_char.get("".join([str(r2), str(new_col2)])))
            elif (c1 == c2): #same column, shift down
                #if its in the last spot, go to col zero (very left side)
                new_row1 = r1 + 1 if r1 + 1 < self.__size else 0
                final.append(self.__pos_to_char.get("".join([str(new_row1), str(c1)])))

                new_row2 = r2 + 1 if r2 + 1 < self.__size else 0
                final.append(self.__pos_to_char.get("".join([str(new_row2), str(c2)])))
            else:
                new_row1 = r1
                new_col1 = c2
                final.append(self.__pos_to_char.get("".join([str(new_row1), str(new_col1)])))

                new_row2 = r2
                new_col2 = c1
                final.append(self.__pos_to_char.get("".join([str(new_row2), str(new_col2)])))

        final = "".join(final)
        return final.encode()
    
    '''
    performs a playfair decryption
    :param ciphertext: the byte array to decrypt
    :return: string of decrypted text 
    '''
    def decrypt(self, ciphertext:bytes) -> str:
        '''
        same as encrypt but shift left and shift up
        '''
        
        #check for good input
        if not(type(ciphertext) is bytes):
            print("Error: bad input")
            quit()

        #parse input
        ciphertext = ciphertext.decode()

        ctemp = ciphertext
        ciphertext = []

        for i in ctemp:
            if i.isalnum():
                ciphertext += i

        ciphertext = "".join(ciphertext)

        #divide ciphertext
        ciphertext = [c for c in ciphertext]

        final = []    
        
        for i in range(0, len(ciphertext), 2):
            #separate into bigrams
            b1 = ciphertext[i]
            b2 = ciphertext[i + 1]

            #get rows and cols
            r1 = self.__char_to_row.get(b1)
            c1 = self.__char_to_col.get(b1)

            r2 = self.__char_to_row.get(b2)
            c2 = self.__char_to_col.get(b2)

            if (r1 == r2): #same row, shift left
                #if its in the last spot, go to col zero (very left side)
                new_col1 = c1 - 1 if c1 - 1 >= 0 else self.__size - 1
                final.append(self.__pos_to_char.get("".join([str(r1), str(new_col1)])))

                new_col2 = c2 - 1 if c2 - 1 >= 0 else self.__size - 1
                final.append(self.__pos_to_char.get("".join([str(r2), str(new_col2)])))
            elif (c1 == c2): #same column, shift down
                #if its in the last spot, go to col zero (very left side)
                new_row1 = r1 - 1 if r1 - 1 >= 0 else self.__size - 1
                final.append(self.__pos_to_char.get("".join([str(new_row1), str(c1)])))

                new_row2 = r2 - 1 if r2 - 1 >= 0 else self.__size - 1
                final.append(self.__pos_to_char.get("".join([str(new_row2), str(c2)])))
            else:
                new_row1 = r1
                new_col1 = c2
                final.append(self.__pos_to_char.get("".join([str(new_row1), str(new_col1)])))

                new_row2 = r2
                new_col2 = c1
                final.append(self.__pos_to_char.get("".join([str(new_row2), str(new_col2)])))

        for i in final:
            if i == "x":
                final.remove(i)

        final = "".join(final)
        return final
    
    '''
    encodes the password in a JSON
    :return: JSON-encoded password
    '''
    def encode_keys(self) -> dict[str,str]:
        return json.dumps({"password": self.__pwd})