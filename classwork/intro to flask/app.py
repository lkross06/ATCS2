from flask import Flask, request, render_template, send_from_directory, send_file

app = Flask(__name__) #create instance of flask object

@app.route("/") #map url route to function
def home(): #the stuff on the webpage
    return "Hello, I am a machine."

@app.route("/url/<username>") #<username> is variable
def user(username):
    return "url-encoded data " + username

@app.route("/jinja/")
def jinja():
    name = request.args.get("name")
    return render_template('hello.html', user=name, items=["evrit", "luckis", "jare id", "vin"])

@app.errorhandler(404)
def error():
    return "This page does not exist :("

if __name__ == "__main__": #if run from terminal
    app.run(port=2020) #run on port 2020