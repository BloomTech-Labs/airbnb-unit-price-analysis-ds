import os
import psycopg2
import simplejson as json
import numpy as np
import pandas as pd
from dotenv import load_dotenv, find_dotenv


load_dotenv() #load database credentials
DB_NAME=os.getenv("DB_NAME")
DB_USERNAME=os.getenv("DB_USERNAME")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_HOST=os.getenv("DB_HOST")


class dbConnector():
    """Class that connects to database"""
    def __init__(self):
        self.Helper = Helper()
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
        data = self.Helper.key_value_query(query, cols)
        return data


    def get_pricing(self) -> list:
        """Retrieves all pricing information for listing id. Meant for /pricing route"""
        sql = f"SELECT * FROM calendar WHERE calendar.listing_id = {self.id}"
        query = self._fetch_query(sql)
        cols = self._get_cols('calendar')
        data = self.Helper.key_value_query(query, cols)
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
        data = self.Helper.key_value_query(query, cols)
        return data


    def get_percentile_totals(self, filter, zipcode, property_type):
        if filter == "z":
            data = [int(word[0]) for word in self._fetch_query(f"""SELECT price FROM listing WHERE zipcode = {zipcode}""")]
        elif filter == "p":
            data = [int(word[0]) for word in self._fetch_query(f"""SELECT price FROM listing WHERE property_type = '{property_type}' """)]
        elif filter == "zp":
            data = [int(word[0]) for word in self._fetch_query(f"""SELECT price FROM listing WHERE property_type = '{property_type}' AND zipcode = {zipcode}""")]
        return data


    def _fetch_query(self, query:tuple) -> tuple:
        """Establishes database connection and executes query
        Returns - Tuple of data"""
        cursor = self.open_connection()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    


class Helper():
    def __init__(self, *args, **kwargs):
        return
    

    def percents(self, listing_price: float, pricing: list):
        prices = [int(price[0]) for price in pricing]
        preds = [np.percentile(prices, x) for x in range(10, 110, 10)]
        places = [num for num in range(10, 100, 10)]
         # Find where listing lies in percentile range
        response = {}
        listing_percentile = np.percentile(places,listing_price)
        response.update({'precentiles':preds})
        response.update({'listing_percentile':listing_percentile})
        return response


    def percentile_totals(self, percentiles, data):
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
        
        return totals

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


    def amens(self, listing_amens: list, total_amens: list, price:float):
        listing_amens = self.json_to_list(listing_amens[0])
        premium_amens = [word[1] for word in total_amens if word[0] > price]
        premium_amens = self.json_to_list(premium_amens)
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


    def json_to_list(self, current_data):
        new = []
        for data in current_data:
            data = data.replace("{", "").replace("}", "").replace('"', "")
            data = data.split(",")
            new.append(data)
        return new


