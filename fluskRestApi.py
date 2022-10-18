from flask import Flask, render_template
from flask_cors import CORS
#from facades.AnonymousFacade import AnonymousFacade
#from data_access_objects.DbRepoPool import DbRepoPool

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/abc")
def get_abc():
    return {"success":"True"}
app.run(debug=True)

