from flask import Flask, request, Response, abort
from sql_manager import *

import json

app = Flask('http_server')


@app.errorhandler(404)
def page_not_found(e):
    resp = Response("No record with that id (404)", status=404)
    return resp

@app.errorhandler(500)
def page_not_found(e):
    resp = Response("INTERNAL SERVER ERROR (500)", status=500)
    return resp


@app.route("/<table_name>/", methods=['GET', 'POST'])
def table(table_name):
    if request.method == 'GET':
        limit = request.args.get('limit', default=5)
        offset = request.args.get('offset', default=0)
        result = get_items(table_name, limit, offset)
        resp = Response(result, mimetype='application/json')
        return resp

    if request.method == 'POST':
        dict = request.get_json()
        list = []
        for i in dict:
            new_list = []
            if type(i) is dict:
                for j in i:
                    new_list.append(str(i[j]))
                list.append(tuple(new_list))
            else:
                list.append(dict[i])
        if isinstance(list[0], str):
            new_list = tuple(list)
            list = []
            list.append(new_list)
        post_many(table_name, list)
        return "Success"


@app.route("/")
def root():
    result = show_tables()
    resp = Response(result)
    resp.headers['Access-Controll-Allow-Origin']='*'
    return resp


@app.route("/test/", methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        return "It's test"
    if request.method == 'POST':
        dict = request.get_json()
        list = []
        for i in dict:
            new_list = []
            new_list.append(i)
            list.append(tuple(new_list))
        print(list)
        return "Success"


@app.route("/<table_name>/<int:id>/", methods=['GET', 'PUT', 'DELETE'])
def row(table_name, id):
    if request.method == 'GET':
        result = get_row(table_name, id)
        if result == '[]':
            abort(404)
        else:
            resp = Response(result, mimetype='application/json')
            return resp
    if request.method == 'PUT':
        dict = request.get_json()
        outer_list = []
        inner_list = []
        for i in dict:
            inner_list.append(str(i))
            inner_list.append(str(dict[i]))
            inner_list.append(id)
            outer_list.append(tuple(inner_list))
        if len(outer_list) == 1:
            outer_list = outer_list[0];

        print(outer_list)

        update(table_name, outer_list)
        return "Table updated"
    if request.method == 'DELETE':
        delete(table_name, id)
        return "Value deleted"


if __name__ == '__main__':
    app.run()