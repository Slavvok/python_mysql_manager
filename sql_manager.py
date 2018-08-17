import mysql.connector
from mysql.connector import Error
import json


def conn(query, is_change=False, data=(), is_one = False, keys=[]):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='mysqldb'
        )
    except Error as e:
        return "Connection failed: " + e
    cur = conn.cursor()
    if is_one:
        cur.execute(query, data)
        conn.commit()
        cur.close()
        return
    if not is_change:
        cur.execute(query)
    if keys:
        count=0
        for i in data:
            cur.execute(query.format(key=keys[count]), i)
            conn.commit()
            count += 1
        cur.close()
        return
    if is_change:
        cur.executemany(query, data)
        conn.commit()
        cur.close()
        return

    field_names = [i[0] for i in cur.description]
    res = cur.fetchall()
    json_data = []
    for id in res:
        json_data.append(dict(zip(field_names, id)))
    return json.dumps(json_data)
    cur.close()

def show_tables():
    return conn("SHOW TABLES FROM mysqldb")

def get_items(table, limit, offset):
    query = "SELECT * FROM {} LIMIT {} OFFSET {}".format(
        table, limit, offset)
    return conn(query)

def get_row(table, id):
    query = "SELECT * FROM {} WHERE id={}".format(
        table, id)
    return conn(query)

def post(table, values):
    vals = ', '.join('%s'.format(i) for i in values[0])
    query = "INSERT INTO " + table + " VALUES ({})".format(vals)
    print(query)
    print(values)
    return conn(query, True, values)

def update(table, keys, values):
    query = "UPDATE "+table+" SET {key}=%s WHERE id=%s"
    return conn(query, True, values, False, keys)

def delete(table, id):
    query = "DELETE FROM "+table+" WHERE id=%s"
    data = (id, )
    return conn(query, False, data, True)

'''
Taking keys from json.

    for i in json.loads(result):
        tables.append(i[key])
    return tables
'''
