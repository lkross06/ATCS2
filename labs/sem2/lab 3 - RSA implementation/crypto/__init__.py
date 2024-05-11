from .rsa import RSA
from .caesar import Caesar
from .playfair import PlayFair
from .vigenere import Vigenere

__all__ = {
    "caesar": Caesar,
    "playfair": PlayFair,
    "rsa": RSA,
    "vigenere": Vigenere
}

'''
returns the requested cipher object with the given password
(or generates a password if none are supplied)

:param name: name of cipher (one of the supported ciphers above)
:param password: password to use (if none, the cipher generates one)

:return: cipher object
'''
def get_cipher(name:str, password:dict = None):
    try:
        return __all__[name](password)
    except:
        return None

'''
formats and returns a string containing the names of all supported ciphers

:return: string of all cipher names, space-separated
'''
def format_ciphers() -> str:
    rtn = []
    for i in __all__.keys():
        rtn.append(i)
    
    return " ".join(rtn).strip()