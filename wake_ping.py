from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/ping")
def home():
    return "Bot is Alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

def ping():
    t = Thread(target=run)
    t.start()