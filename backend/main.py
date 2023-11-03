from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)


def get_db():
    client = MongoClient(
        host='mongo',
        port=27017,
        username='root',
        password='pass',
        authSource='admin'
    )
    db = client.records
    return db


@app.route("/")
def hello_world():
    db = get_db()
    values = db.values
    values.insert_one({"test": "test", })
    count = values.count_documents({})
    return f"<p>{count}</p>"
