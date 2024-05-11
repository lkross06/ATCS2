from flask import Flask, redirect, send_file, request, render_template

app = Flask(__name__)

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return redirect("/static/login.html")
    else: #POST method
        username = request.form.get("username")
        password = request.form.get("password")
        mode = request.form.get("mode")
        print(username, password, mode)
        return "SUCCESS"

@app.route("/logout")
def logout():
    return "SUCCESS"

@app.route("/profile", methods=["POST", "GET"])
def profile():
    if request.method == "GET":
        return redirect("/static/profile.html")
    else:
        action = request.form.get("action")
        print(action, request.form.get(action))
        return "SUCCESS" 
    
@app.route("/files", methods=["POST"])
def files():
    action = request.form.get("action")
    print(action, request.form.get(action))
    return "SUCCESS" 
    

if __name__ == "__main__":
    app.run(port=8022)