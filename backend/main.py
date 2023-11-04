from typing import Callable, Optional

from flask import Flask, request, Response
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

DB_HOST: str = 'mongo',
DB_PORT: int = 27017
DB_USERNAME: str = 'root'
DB_PASSWORD: str = 'pass'
DB_NAME: str = 'records'
TABLE_NAME: str = 'values'


app = Flask(__name__)


def get_table() -> Collection:
    client = MongoClient(
        host=DB_HOST,
        port=DB_PORT,
        username=DB_USERNAME,
        password=DB_PASSWORD,
        authSource='admin'
    )
    db: Database = client[DB_NAME]
    table: Collection = db[TABLE_NAME]
    return table


def get_value(data: dict) -> Response:
    table: Collection = get_table()
    key = data.get('key')
    if key is not None:
        filter_criteria = {key: {'$exists': True}}
        answer = table.find_one(filter_criteria)
        if answer is not None:
            return Response(f'{key} = {answer[key]}', status=200)
    return Response('Запись не найдена', status=404)


def add_value(data: dict) -> Response:
    if data:
        key = data["key"]
        value = data["value"]
        table: Collection = get_table()
        table.insert_one({key: value})
        return Response(f'{key} = {value}', status=201)
    return Response('Запрос не содержит данных', status=400)


def edit_or_add_value(data: dict) -> Response:
    if data:
        table: Collection = get_table()
        key = data.get('key')
        new_value = data.get('value')
        filter_criteria = {key: {'$exists': True}}
        if table.find_one(filter_criteria) is not None:
            update_data = {'$set': {key: new_value}}
            table.update_one(filter_criteria, update_data)
            return Response(f'{key} = {new_value}', status=200)
        else:
            table.insert_one({key: new_value})
            return Response(f'{key} = {new_value}', status=201)
    return Response('Запрос не содержит данных', status=400)


def get_action(method: str) -> Optional[Callable]:
    methods = {
        'POST': add_value,
        'GET': get_value,
        'PUT': edit_or_add_value
    }
    return methods.get(method)


@app.route('/', methods=['POST', 'GET', 'PUT'])
def handle_requests() -> Response:
    data = request.get_json()
    return get_action(request.method)(data)
