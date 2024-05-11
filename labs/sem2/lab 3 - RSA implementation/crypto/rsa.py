import pickle
import random
import math

class RSA:
    '''
    creates a new RSA cipher object
    
    :param keys: the JSON-encoded public and private keys. if not specified,
    then p and q are randomly generated and e, d, and n are calculated
    '''
    def __init__(self, keys:dict[str,tuple] = None):
        self.__NUMBITS = 1024 #used 8 for testing purposes

        valid_keys = keys != None

        self.__e = None
        self.__d = None
        self.__n = None

        if valid_keys:
            if keys.get("public") != None:
                self.__e = keys.get("public")[0]
                self.__n = keys.get("public")[1]
            else:
                valid_keys = False
            
            if keys.get("private") != None:
                self.__d = keys.get("private")[0]
                self.__n = keys.get("private")[1]
            else:
                valid_keys = False

        if not(valid_keys):   
            p, q = self.__generate_primes()
            self.__n = p * q
            self.__totientN = (p - 1) * (q - 1)
            self.__e = self.__find_e()
            self.__d = self.__find_d()

    '''
    reads the file specific to the type of expected file data

    :param i: the input file path
    :param mode: the mode (expecting "encrypt" or "decrypt")

    :return: correctly parsed input data, None if not found
    '''
    def read_file(self, i:str, mode:str):
        try:
            if mode == "encrypt":
                with open(i, "r") as file:
                    return "".join([str(x).removesuffix("\n") for x in file.readlines()])

            elif mode == "decrypt":
                with open(i, "rb") as file:
                    return pickle.load(file)
                
            return None
        except:
            return None

    '''
    performs an RSA encryption on a string by splitting it up into blocks/chunks
    
    :param plaintext: the plaintext to encrypt

    :return: pickle-encoded byte array of encrypted chunks
    '''
    def encrypt(self, plaintext:str) -> bytes:
        #C = P^e % N
        nums = []

        for c in plaintext:
            x = pow(ord(c), self.__e) % self.__n
            nums.append(x)

        return pickle.dumps(nums)

    '''
    performs an RSA decryption on an array of pickle-encoded bytes and finds the string plaintext
    
    :param ciphertext: the ciphertext (pickle-encoded byte array) to decrypt

    :return: decrypted plaintext
    '''
    def decrypt(self, ciphertext:bytes) -> str:
        #P = C^d % N

        pt = []
    
        for b in ciphertext:
            s = chr(pow(b, self.__d) % self.__n)
            pt.append(s)
        return "".join(pt)
    
    '''
    JSON-encodes public and private keys for ease of transferring

    :return: dictionary containing public (e, n) and private (d, n) key tuples 
    '''
    def encode_keys(self) -> dict[str,tuple]:
        return {
            "public": (self.__e, self.__n),
            "private": (self.__d, self.__n)
        }

    def __find_e(self):
        totn = self.__totientN

        for e in range(2, totn): #1 < e < tot(n) - 1
            #math.gcd(a, b) is Euclid's GCD algorithm and checks if tot(N) and e are relatively prime
            if math.gcd(totn, e) == 1: 
                return e
        
        return None
    
    def __ext_euclids_gcd(self, a:int, b:int) -> int:
        #manually perform euclid's GCD and backtracking (i.e. extended euclid's GCD) simultaneously.

        if a == b:
            return None
        
        #euclids gcd
        r = a % b
        q = a // b

        #extended euclids gcd
        t1 = 0
        t2 = 1
        t3 = t1 - (q * t2)

        while r > 0:

            a = b
            b = r
            r = a % b
            q = a // b

            t1 = t2
            t2 = t3
            t3 = t1 - (q * t2)

        # if s2 * a + t2 * b = gcd(a, b) then d (for RSA) = t2
        #if a and b are relatively prime then r = 0
        if r == 0:
            return t2
        return None

    def __find_d(self):
        totn = self.__totientN
        e = self.__find_e()

        d = self.__ext_euclids_gcd(totn, e)
        if d != None and d < 0:
            d += totn #if d < 0 then d += tot(N)
        
        return d
        
    def __generate_primes(self) -> int:
    
        def __rabinMiller(num):
            # inventwithpython.com (BSD License)

            # Returns True if num is a prime number.

            s = num - 1
            t = 0
            while s % 2 == 0:
                # keep halving s while it is even (and use t
                # to count how many times we halve s)
                s = s // 2
                t += 1

            # Increase the trials to improve probability
            # Anything over 40 is mathematically not worth the computation
            for trials in range(5): # try to falsify num's primality 5 times
                a = random.randrange(2, num - 1)
                v = pow(a, s, num)
                if v != 1: # this test does not apply if v is 1.
                    i = 0
                    while v != (num - 1):
                        if i == t - 1:
                            return False
                        else:
                            i = i + 1
                            v = (v ** 2) % num
            return True
        
        #get p
        p = None
        while p == None:
            n = random.getrandbits(self.__NUMBITS)

            #only evaluate odd numbers (cuts the number of rabin miller function calls in half)
            if n % 2 == 1:
                if __rabinMiller(n): #check primality
                    p = n

        #get q
        q = None
        while q == None:
            n = random.getrandbits(self.__NUMBITS)

            if n % 2 == 1:
                if __rabinMiller(n): #check primality
                    q = n

        return p, q