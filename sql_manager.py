import mysql.connector
import json

def conn(query, is_change=False, data=(), is_one = False):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='mysqldb'
        )
    except Exception:
        return ("Connection failed")
    cur = conn.cursor()
    if (is_one):
        cur.execute(query, data)
        conn.commit()
        cur.close()
        return
    if (not is_change):
        cur.execute(query)
    if (is_change):
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

def get_text(table, id):
    query = "SELECT * FROM {} WHERE id={}".format(
        table, id)
    return conn(query)

def post(table, id, text):
    query = "INSERT INTO "+table+" VALUES (%s, %s)"
    data = (id, text)
    return conn(query, True, data)

def post_many(table, values):
    query = "INSERT INTO " + table + " VALUES (%s, %s)"
    print(query)
    print(values)
    return conn(query, True, values)

def update(table, values):
    query = "UPDATE "+table+" SET %s=%s WHERE id=%s"
    return conn(query, True, values)

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
