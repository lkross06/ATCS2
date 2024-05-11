import os
import json

'''
user login credentials
'''
class Account:
    def __init__(self):
        self.username = ""
        self.password = "" #sha256 hashed salt + password
        self.salt = "" #10-character salt

'''
profile details
'''
class Profile:
    def __init__(self):
        self.username = ""
        self.fname = ""
        self.lname = ""
        self.avatar = "static/default.jpg"
        self.files = ""
    
    '''
    exports profile as json to be read by jinja2

    :return: json-encoded profile
    '''
    def jsonify(self) -> dict:
        return {
            "username":self.username,
            "fname":self.fname,
            "lname":self.lname,
            "avatar":self.avatar,
            "files":self.files
        }
    
    '''
    exports profile as string

    :return: json-serialized object to string
    '''
    def __str__(self) -> str:
        return json.dumps(self.jsonify())