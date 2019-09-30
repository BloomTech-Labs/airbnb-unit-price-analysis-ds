import os
import psycopg2
import simplejson as json
import numpy as np
from flask import Flask, request, jsonify
from dotenv import load_dotenv, find_dotenv


application = app = Flask(__name__) #application name for AWS beanstalk

load_dotenv() #load database credentials
DB_NAME=os.getenv("DB_NAME")
DB_USERNAME=os.getenv("DB_USERNAME")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_HOST=os.getenv("DB_HOST")



@application.route('/data')
def data():
    """Retrieve all listings associated with the passed id"""
    id = request.args.get('id')
    db = dbConnector()
    db.set_id(id)
    data = db.get_listing()
    return json.dumps(data,use_decimal=True)


@application.route('/preds')
def preds():
    """Retrieve all listings associated with the passed id and returns predicted price"""
    id = request.args.get('id')
    db = dbConnector()
    db.set_id(id)
    data = db.get_listing()
    zipcode = data[0]['zipcode']
    preds = db.predictions(zipcode)
    return json.dumps(preds, use_decimal=True)


class dbConnector():
    """Class that connects to database"""
    def __init__(self):
        return

    def set_id(self, id:str):
        self.id = id


    def open_connection(self):
        """Establish connection with RDS"""
        connection = psycopg2.connect(dbname=DB_NAME, 
                                user=DB_USERNAME, 
                                password=DB_PASSWORD, 
                                host=DB_HOST,
                                port=5432)
        cursor = connection.cursor()
        return cursor


    def get_listing(self) -> list:
        """Retrieves all listing information for specific id. Meant for /data route"""

        sql = f"SELECT * FROM listing WHERE listing.id = {self.id}"
        query = self._fetch_query(sql)
        cols = self._get_cols('listing')
        data = self.key_value_query(query, cols)
        return data


    def get_pricing(self) -> list:
        """Retrieves all pricing information for listing id. Meant for /pricing route"""
        sql = f"SELECT * FROM calendar WHERE calendar.listing_id = {self.id}"
        query = self._fetch_query(sql)
        cols = self._get_cols('calendar')
        data = self.key_value_query(query, cols)
        return data


    def _get_cols(self, table:str) -> tuple:
        """Retrieves all column names for a specific table"""
        sql = f'''SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = '{table}' '''

        columns = self._fetch_query(sql)
        return columns


    def _fetch_query(self, query:tuple) -> tuple:
        """Establishes database connection and executes query
        Returns - Tuple of data"""
        cursor = self.open_connection()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data


    def key_value_query(self, query:tuple, cols:tuple) -> list:
        """Returns key value pairs:
        Returns - list of {Column Name : Value}"""
        for listing, col in zip(query, cols):
            temp = {}
            lists = []
            i=0
            while i < len(listing):
                temp[cols[i][0]] = listing[i]
                i+=1
                lists.append(temp)
        return lists


    def predictions(self, zipcode):
        cursor = self.open_connection()
        cursor.execute(f"""SELECT price FROM listing WHERE zipcode = '{zipcode}' """)
        data = [int(word[0]) for word in cursor.fetchall()]
        preds = [np.percentile(data, x) for x in range(10, 110, 10)]

        return preds


if __name__ == '__main__':
    app.run(debug=True)
