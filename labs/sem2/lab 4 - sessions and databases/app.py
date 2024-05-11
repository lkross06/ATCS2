from flask import Flask, redirect, send_file, request, render_template, make_response
from db_manager import *
import os

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
            new_loc = os.path.join("static/avatars", "".join([user, ".", ext]))

            picture.save(new_loc) #save locally

            profile_update(token=token, username=user, avatar=new_loc)

        elif action == "name":
            fname = request.form.get("fname")
            lname = request.form.get("lname")
            profile_update(token=token, username=user, fname=fname, lname=lname)
        elif action == "delete":
            confirmation = request.form.get("confirmation")
            if confirmation == user:
                #invalidate tokens and delete the profile
                profile_delete(user)
                session_delete(token)

                response = make_response(redirect("/login"))
                response.set_cookie("token", "", max_age=0) #delete cookie

                return response
            
        profile = session_get(token) #get the updated profile

        return render_template("profile.j2", profile=profile, files=os.listdir(profile.files), show_options=True)

@app.route("/<user>/files", methods=["POST"])
def user_files(user):
    token = request.cookies.get("token")

    if token != None:
        try:
            file = request.files["file"]
                    
            full_path = session_get(token).files
            file.save(os.path.join(full_path, file.filename)) #save locally

            return redirect(f"/{user}/profile")
        except:
            return redirect(f"/{user}/profile")
    else:
        return redirect("/")

if __name__ == "__main__":
    app.run(port=8022)