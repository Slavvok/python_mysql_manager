from flask import Flask, request, Response
from sql_manager import *

import json

app = Flask('http_server')

@app.errorhandler(404)
def page_not_found(e):
    resp = Response("404")
    return resp

@app.route("/<table_name>/", methods=['GET','POST'])
def table(table_name):
    if request.method == 'GET':
        limit = request.args.get('limit', default=5)
        offset = request.args.get('offset', default=0)
        result = get_items(table_name, limit, offset)
        resp = Response(result)
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

@app.route("/test/", methods = ['GET', 'POST'])
def test():
    if request.method == 'GET':
        return "It's test"
    if request.method == 'POST':
        dict = request.get_json()
        list = []
        for i in dict:
            new_list = []
            for j in i:
                new_list.append(i[j])
            list.append(tuple(new_list))
        print(list)
        return "Success"

@app.route("/<table_name>/<int:id>/", methods=['GET', 'PUT', 'DELETE'])
def tableE(table_name, id):
    if request.method == 'GET':
        result = get_text(table_name, id)
        resp = Response(result)
        return resp
    if request.method == 'PUT':
        dict = request.get_json()
        outer_list = []
        inner_list = []
        for i in dict:
            inner_list.append(i)
            inner_list.append(dict[i])
            inner_list.append(str(id))
            outer_list.append(tuple(inner_list))
        if len(outer_list) == 1:
            outer_list = outer_list[0];

        print(outer_list)

        update(table_name, id, outer_list)
        return "Table updated"
    if request.method == 'DELETE':
        delete(table_name, id)
        return "Value deleted"

if __name__ == '__main__':
    app.run()