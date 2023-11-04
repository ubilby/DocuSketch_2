from typing import Callable, Optional

from flask import Flask, request
from pymongo import MongoClient


DB_HOST = 'mongo',
DB_PORT = 27017
DB_USERNAME = 'root'
DB_PASSWORD = 'pass'
DB_NAME = 'records'
TABLE_NAME = 'values'

app = Flask(__name__)


def get_table():
    client = MongoClient(
        host=DB_HOST,
        port=DB_PORT,
        username=DB_USERNAME,
        password=DB_PASSWORD,
        authSource='admin'
    )
    db = client[DB_NAME]
    table = db[TABLE_NAME]
    return table


def get_value(value: dict) -> None:
    return 'GET'


def add_value(value: dict) -> None:

    return 'POST'


def edit_or_add_value(value: dict) -> None:

    return 'PUT'


def get_action(method: str) -> Optional[Callable]:
    methods = {
        'POST': add_value,
        'GET': get_value,
        'PUT': edit_or_add_value
    }
    return methods.get(method)


@app.route('/', methods=['POST', 'GET', 'PUT'])
def handle_requests():
    values = get_table()
    values.insert_one({'test': 'test', })
    count = values.count_documents({})
    data = request.get_json()
    return get_action(request.method)(data)
