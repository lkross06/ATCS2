from flask import Flask, redirect, send_file, send_from_directory, request, render_template, make_response
from db_manager import *
import os
import requests
import socket

'''
gets the correct error message to display based on error type

:param type: type of error (shorthand for message)

:return: error message
'''
def error_message_get(type:int) -> str:
    if type == 1:
        return "incorrect username or password"
    elif type == 2:
        return "username already exists"
    elif type == 3:
        return "invalid request"
    elif type == 4:
        return "not logged in"
    
    return "please try again"

'''
generates a random password so we aren't actually sending profiles across the LAN

:return: randomly-generated alphanumeric password
'''
def generate_random_password() -> str:
    #same as generate salt code
    __ASCII_NUM_START = 48 #used for generated random alphanumeric symbols
    __ASCII_NUM_END = 57
    __ASCII_ALPHA_START = 97
    __ASCII_ALPHA_END = 122
    __SALT_LENGTH = 10 #10 random characters

    alphanum = [chr(x) for x in range(__ASCII_NUM_START, __ASCII_NUM_END+1)] + [chr(x) for x in range(__ASCII_ALPHA_START, __ASCII_ALPHA_END+1)]
    salt = "".join([random.choice(alphanum) for x in range(__SALT_LENGTH)])
    return salt

FLASK_PORT = 8022

app = Flask(__name__)


@app.route("/")
def home():
    token = request.cookies.get("token")
    prof = session_get(token)
    if token == None: #not logged in
        return redirect("/login")
    if prof == None: #previous token exists but not logged in
        resp = make_response(
            redirect("/login"))
        resp.set_cookie(token, "", max_age=0)
        return resp
    
    user = prof.username
    return redirect(f"/{user}/profile")

@app.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "POST":
        mode = request.form.get("mode")
        username = request.form.get("username")
        password = request.form.get("password")
        if mode == "login":
            if account_auth(username, password): #check the database for correct account info
                prof = profile_get(username) #get from sql
                
                #log in
                response = make_response(redirect(f"/{username}/profile"))
                token = session_set(prof) #create a session token and store profile in redis
                response.set_cookie(key="token", value=token)

                return response
            else:
                return render_template("login.j2", error_message=error_message_get(1)) #invalid login
        elif mode == "register":
            if profile_get(username) != None: #check to see if account with that username exists
                return render_template("login.j2", error_message=error_message_get(2)) #username already exists
            
            #create account
            prof = account_create(username, password)
            token = session_set(prof) #generate a uuidv4 token

            response = make_response(redirect(f"/{username}/profile"))
            response.set_cookie(key="token", value=token)

            #send the new account/profile
            if not(request.form.get("foreign")):
                for client in connections_get():
                    try:
                        url = f"http://{client}:{FLASK_PORT}/login"
                        form_data = {
                            "foreign":True,
                            "mode":"register",
                            "username":username,
                            "password":generate_random_password() #don't wanna send actual password...
                        }
                        requests.post(url=url, data=form_data)
                        print(f"sent account create request to {client}")
                    except:
                        print(f"couldn't send account create request to {client}")
                        continue #couldn't connect

            return response
        
        else:
            return "FAILURE"
    else:
        return render_template("login.j2", error_message=None)
    
@app.route("/logout", methods=["POST"])
def logout():
    token = request.cookies.get("token")

    session_delete(token)

    response = make_response(redirect("/"))
    response.set_cookie("token", "", max_age=0) #delete cookie

    return response

@app.route("/<user>/profile", methods=["POST", "GET"])
def user_profile(user):
    token = request.cookies.get("token")
    is_logged_in = token != None

    if is_logged_in:
        profile = session_get(token) #get from redis (active profile)
        if profile == None:
            #you need to log in to see profiles
            return render_template("login.j2", error_message=error_message_get(4))
    else:
        return render_template("login.j2", error_message=error_message_get(4))

    if request.method == "GET":
        is_personal_profile = True

        #profile from token doesn't match URL username
        if profile.username != user:
            profile = profile_get(user) #get from sql (non-active profile)
            is_personal_profile = False

        if profile == None:
            return redirect("/") #profile in URL doesn't exist

        return render_template("profile.j2", profile=profile, files=os.listdir(profile.files), show_options=is_personal_profile)
    else:
        action = request.form.get("action")

        if action == "password":
            password = request.form.get("password")
            account_update_password(user, password) #server side only
        elif action == "picture":
            picture = request.files["picture"]

            ext = picture.filename.split(".")[1] #get file type (i.e. png, jpg, etc.)
            new_loc = os.path.join("avatars", "".join([user, ".", ext]))

            picture.save(new_loc) #save locally

            profile_update(token=token, username=user, avatar=new_loc)

        elif action == "name":
            fname = request.form.get("fname")
            lname = request.form.get("lname")
            profile_update(token=token, username=user, fname=fname, lname=lname)
            
        profile = session_get(token) #get the updated profile

        return render_template("profile.j2", profile=profile, files=os.listdir(profile.files), show_options=True)

@app.route("/<user>/profile/delete", methods=["POST"])
def delete_profile(user):
    action = request.form.get("action")

    if action == "delete":
        confirmation = request.form.get("confirmation")
        if confirmation == user:
            #invalidate tokens and delete the profile
            profile_delete(user)
            token = request.cookies.get("token")
            if token != None: #if its a foreign request then no need
                session_delete(token)

        #send delete profile request 
        if not(request.form.get("foreign")):   
            for client in connections_get():
                try:
                    url = f"http://{client}:{FLASK_PORT}/{user}/profile/delete"
                    form_data = {
                        "foreign":True,
                        "action":"delete",
                        "confirmation":confirmation
                    }
                    requests.post(url=url, data=form_data)
                    print(f"sent account delete request to {client}")
                except:
                    print(f"couldn't send account delete request to {client}")
                    continue #couldn't connect

        response = make_response(redirect("/login"))
        response.set_cookie("token", "", max_age=0) #delete cookie

        return response
    
    return redirect(f"/{user}/profile")

@app.route("/<user>/file/upload", methods=["POST"])
def upload_file(user):
    try:
        file = request.files["file"]
        
        full_path = os.path.join(os.getcwd(), "files", user, file.filename)
        file.save(full_path) #save locally

        #send uploaded file to others
        if not(request.form.get("foreign")):
            with open(full_path, "rb") as f:
                for client in connections_get():
                    try:
                        url = f"http://{client}:{FLASK_PORT}/{user}/file/upload"
                        requests.post(url=url, files={"file":f}, data={"foreign":True})
                        print(f"sent file upload request to {client}")
                    except:
                        print(f"couldn't send file upload request to {client}")
                        continue #couldn't connect

        return redirect(f"/{user}/profile")
    except:
        return redirect(f"/{user}/profile")
    
@app.route("/<user>/file/delete/<file>", methods=["POST"])
def delete_file(user, file):
    path = os.path.join(os.getcwd(), "files", user, file)
    if os.path.exists(path):
        os.remove(path)

    #send deleted file action to others
    if not(request.form.get("foreign")):
        for client in connections_get():
            try:
                url = f"http://{client}:{FLASK_PORT}/{user}/file/delete/{file}"
                requests.post(url=url, data={"foreign":True}) #let the other pc know not to send more requests
                print(f"sent file delete request to {client}")
            except:
                print(f"couldn't send file delete request to {client}")
                continue #couldn't connect

    return redirect(f"/{user}/profile")

@app.route("/<user>/file/download/<file>")
def download_file(user, file):
    return send_from_directory(f"files/{user}", file, as_attachment=True)

if __name__ == "__main__":
    try:
        __MY_HOSTNAME = socket.gethostname()
        __MY_IP = socket.gethostbyname(__MY_HOSTNAME)

        #sometimes it just gives the loopback address
        if __MY_IP == "127.0.0.1": 
            #get more info about the IP and retrieve the true ipv4 address
            __MY_IP = socket.gethostbyname_ex(__MY_HOSTNAME)[2][1]
        
        app.run(host=__MY_IP, port=FLASK_PORT) #MUST have host=ip to send requests across network
    except socket.gaierror:
        print("Error: could not resolve hostname")
    except Exception as e:
        print(f"Error: {e}")
        