from flask import Flask, render_template
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))

@app.route("/")
def landing():
    return render_template("landing.html")

if __name__ == "__main__":
    app.run(port=5001, debug=False)