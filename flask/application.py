<<<<<<< HEAD
import os
import psycopg2
import simplejson as json
from flask import Flask, request, jsonify
from dotenv import load_dotenv, find_dotenv


application = app = Flask(__name__) #application name for AWS beanstalk

load_dotenv() #load database credentials
DB_NAME=os.getenv("DB_NAME")
DB_USERNAME=os.getenv("DB_USERNAME")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_HOST=os.getenv("DB_HOST")

=======
import simplejson as json
from flask import Flask, request, jsonify
from helpers import dbConnector, Helper
import numpy as np

application = app = Flask(__name__) #application name for AWS beanstalk

>>>>>>> routes


@application.route('/data')
def data():
<<<<<<< HEAD
    """Retrieve all listings associated with the passed id"""
=======
    """Retrieve all listing features associated with the passed id"""
>>>>>>> routes
    id = request.args.get('id')
    db = dbConnector()
    db.set_id(id)
    data = db.get_listing()
    return json.dumps(data,use_decimal=True)

<<<<<<< HEAD

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
        data =self.key_value_query(query, cols)
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
=======
@application.route('/comparison')
def compare():
    """Retrieve the most popular listing that is similar to the inputed listing"""
    id = request.args.get('id')
    feature = request.args.get('feature')
    db = dbConnector()
    db.set_id(id)
    data = db.get_listing()
    listing_feature = data[0][feature]
    data = db.get_comparison(feature, listing_feature)
    return json.dumps(data,use_decimal=True)


@application.route('/pricing')
def preds():
    """Retrieves 10 percentiles based on listing location"""
    id = request.args.get('id')
    db = dbConnector()
    db.set_id(id)
    data = db.get_listing()
    zipcode = data[0]['zipcode']
    listing_price = data[0]['price']
    prices = db.get_price_by_zip(zipcode)
    preds = db.percents(float(listing_price),prices)
    return json.dumps(preds, use_decimal=True)


@application.route('/amenities')
def amenities():
    """Returns listing amenities and missing amenities that the most popular listings offer"""
    id = request.args.get('id')
    db = dbConnector()
    db.set_id(id)
    data = db.get_listing()
    zipcode = data[0]['zipcode']
    price = data[0]['price']
    listing_amenities = data[0]['amenities']
    total_amenities = db.get_amens_by_zip(zipcode)
    amens = db.amens(listing_amenities, total_amenities,price)
    return json.dumps(amens, use_decimal=True)


@application.route('/percentiles')
def percentiles():
    id = request.args.get('id')
    filter = request.args.get('filter')
    db = dbConnector()
    db.set_id(id)
    data = db.get_listing()
    zipcode = data[0]['zipcode']
    property_type = data[0]['property_type']
    data = db.get_percentile_totals(filter, zipcode, property_type)
    percentiles = [np.percentile(data, x) for x in range(10, 110, 10)]
    totals = db.percentile_totals(percentiles,data)
    return json.dumps(totals,use_decimal=True)

>>>>>>> routes


if __name__ == '__main__':
    app.run(debug=True)
