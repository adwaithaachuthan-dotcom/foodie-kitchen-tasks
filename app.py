import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI")

if not mongo_uri:
    raise ValueError("MONGO_URI is missing from the .env file")

client = MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)

db = client["beginner_db"]
todos_collection = db["todos"]


@app.route("/")
def index():
    todos = list(todos_collection.find())
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add_todo():
    task = request.form.get("task", "").strip()

    if task:
        todos_collection.insert_one({"task": task})

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)