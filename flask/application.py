import os
import psycopg2
import simplejson as json
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from dotenv import load_dotenv, find_dotenv

'''@application.route('/percentiles')
def percentiles(filter_):
    db = dbConnector()
    cursor = db.open_connection()
    if filter_ == "z":
        zipcode = request.args.get('zipcode')
        data = [int(word[0]) for word in cursor.execute("""SELECT price FROM listing WHERE zipcode = {%s}""", [zipcode])]
    elif filter_ == "p":
        property_type = request.args.get('property_type')
        data = [int(word[0]) for word in cursor.execute("""SELECT price FROM listing WHERE property_type = {%s}""", [property_type])]
    elif filter_ == "zp":
        zipcode = request.args.get('zipcode')
        property_type = request.args.get('property_type')
        data = [int(word[0]) for word in cursor.execute("""SELECT price FROM listing WHERE property_type = {%s} AND zipcode = {%s}""", [property_type, zipcode])]
    percentiles = [np.percentile(data, x) for x in range(10, 110, 10)]
    totals = []
    for n, percent in enumerate(percentiles):
        count = 0
        if n == 0:
            for d in data:
                if d <= percent:
                    count += 1
                else:
                    pass
        elif n == 9:
            for d in data:
                if d >= percent:
                    count += 1
                else:
                    pass
        else:
            for d in data:
                if d >= percent and d < percentiles[n+1]:
                    count += 1
                else:
                    pass
        totals.append(count)
        
        
    return percentiles, totals'''

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

@application.route('/comparison')
def compare():
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
    """Retrieve all listings associated with the passed id and returns predicted price"""
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


    def get_price_by_zip(self, zipcode: int) -> list:
        sql = f"""SELECT price FROM listing WHERE zipcode = '{zipcode}' """
        data = self._fetch_query(sql)
        return data
    

    def get_amens_by_zip(self, zipcode: int) -> list:
        sql = f"""SELECT price, amenities FROM listing WHERE zipcode = '{zipcode}' """
        data = self._fetch_query(sql)
        return data


    def _get_cols(self, table:str) -> tuple:
        """Retrieves all column names for a specific table"""
        sql = f'''SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = '{table}' '''

        columns = self._fetch_query(sql)
        return columns
    

    def get_comparison(self, feature:str, listing_feature:str, *args) -> tuple:
        """Retrieves comparison between listing id and most popular listing"""
        sql = f"""SELECT *
                FROM listing as l1 
                WHERE l1.number_of_reviews >= ALL
                    (SELECT AVG(l2.number_of_reviews) as num_reviews 
                    FROM listing as l2 
                    WHERE l2.{feature} = '{listing_feature}'
                    GROUP BY l2.{feature}
                    ORDER BY num_reviews DESC)
                AND l1.{feature} = '{listing_feature}'
                ORDER BY l1.review_scores_rating DESC
                LIMIT 1"""
        query = self._fetch_query(sql)
        cols = self._get_cols('listing')
        data = self.key_value_query(query, cols)
        return data


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


    def percents(self, listing_price: float, pricing: list):
        prices = [int(price[0]) for price in pricing]
        preds = [np.percentile(prices, x) for x in range(10, 110, 10)]
        places = [num for num in range(10, 110, 10)]
        percentiles = {p:perct for p, perct in zip(places, preds)}
         # Find where listing lies in percentile range
        response = {}
        listing_percentile = np.percentile(places,listing_price)
        response.update({'precentiles':preds})
        response.update({'listing_percentile':listing_percentile})
        return response
    

    def amens(self, listing_amens: list, total_amens: list, price:float):
        helper = Helper()
        listing_amens = helper.json_to_list(listing_amens[0])
        premium_amens = [word[1] for word in total_amens if word[0] > price]
        premium_amens = helper.json_to_list(premium_amens)
        higher_amens = []
        for amen in premium_amens:
            for a in amen:
                if a in listing_amens:
                    pass
                else:
                    if a not in higher_amens:
                        higher_amens.append(a)
                    else:
                        pass
        json_amens = {'lacking_amenities':higher_amens}
        return json_amens
        


class Helper():
    def __init__(self, *args, **kwargs):
        return
    

    def json_to_list(self, current_data):
        new = []
        for data in current_data:
            data = data.replace("{", "").replace("}", "").replace('"', "")
            data = data.split(",")
            new.append(data)
        return new


    def unique_amenities(self, df, column):
        amens = higher['amenities'].values
        higher_amenities = json_to_list(higher['amenities'].values)
        higher_amens = []
        for amen in higher_amenities:
            for a in amen:
                if a in amenities:
                    pass
                else:
                    if a not in higher_amens:
                        higher_amens.append(a)
                    else:
                        pass
        json_amens = {'lacking_amenities':higher_amens}
        return json_amens



if __name__ == '__main__':
    app.run(debug=True)
