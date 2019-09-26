from flask import Flask, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv, find_dotenv
import simplejson as json

application = app = Flask(__name__)

load_dotenv()
DB_NAME=os.getenv("DB_NAME")
DB_USERNAME=os.getenv("DB_USERNAME")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_HOST=os.getenv("DB_HOST")



@application.route('/data')
def data():
    id = request.args.get('id')
    data = key_value_query(id)
    return json.dumps(data,use_decimal=True)


def open_connection():
    connection = psycopg2.connect(dbname=DB_NAME, 
                            user=DB_USERNAME, 
                            password=DB_PASSWORD, 
                            host=DB_HOST,
                            port=5432)
    cursor = connection.cursor()
    return cursor


def get_cols():
    sql = '''SELECT column_name 
             FROM information_schema.columns 
             WHERE table_name = 'listing' '''

    cursor = open_connection()
    cursor.execute(sql)
    cols = cursor.fetchall()
    cursor.close()
    return cols


def get_listing(id):
    sql = f"SELECT * FROM listing WHERE listing.id = {id}"
    cursor = open_connection()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    return data


def key_value_query(id):
    listings = get_listing(id)
    cols = get_cols()
    k=0
    for listing, col in zip(listings, cols):
        temp = {}
        lists = []
        i=0
        while i < len(listing):
            temp[cols[i][0]] = listing[i]
            i+=1
            lists.append(temp)
        k+=1
    return lists


if __name__ == '__main__':
    app.run(debug=True)
