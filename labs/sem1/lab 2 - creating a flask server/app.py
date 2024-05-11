from flask import Flask, redirect, send_file, request, render_template
from leaderboard import Leaderboard
from cipher import get_symmetric

app = Flask(__name__)
lb = Leaderboard()

@app.route("/")
def home():
    return redirect("/static/index.htm") #response

@app.route("/minesweeper", methods=["POST", "GET"])
def minesweeper():
    return redirect("/minesweeper/intro.html") #send another request

@app.route("/minesweeper/<path:path>", methods=["POST", "GET"])
def mine_file(path):
    if request.method == "POST":
        lb.add(request.json) #add the game data json to the leaderboard

    return send_file("minesweeper/" + path)

@app.route("/minesweeper/leaders")
def leaderboard():
    return render_template(
        "leaderboard.html",
        items = lb.to_array() #get the leaderboard
    )

#-------------------------- 

@app.route("/crypto/symmetric", methods=["GET"])
def symm_get():
    return redirect("/crypto/symmetric.html")

@app.route("/crypto/symmetric", methods=["POST"])
def symm_post():
    cipher = request.form.get("cipher")
    mode = request.form.get("mode")
    message = request.form.get("message")
    password = request.form.get("password")

    result = get_symmetric(cipher, mode, message, password)
    return result

@app.route("/crypto/steg", methods=["GET"])
def steg_get():
    return redirect("/crypto/steg.html")

@app.route("/crypto/steg", methods=["POST"])
def steg_post():
    cd_type = request.form.get("cd")

    cd = None
    if cd_type == "text":
        cd = request.form.get("cd_textin")
    elif cd_type == "image":
        cd = request.files["cd_imagein"]
        if cd.filename == "":
            cd = None

    host = None
    host = request.files["host"]
    if host.filename == "":
        host = None

    if not(cd_type == None and cd == None and host == None):
        print(cd_type, cd.filename, host.filename)
        return "SUCCESS"
    
    return "FAILURE"

@app.route("/crypto/<path:path>")
def crypto_file(path):
    return send_file("crypto/" + path)

if __name__ == "__main__":
    app.run(port=4242)