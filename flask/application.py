import simplejson as json
from flask import Flask, request, jsonify
from helpers import dbConnector, Helper
import numpy as np
from flask_cors import CORS

application = app = Flask(__name__) #application name for AWS beanstalk
CORS(application)


@application.route('/data')
def data():
    """Retrieve all listing features associated with the passed id"""
    id = request.args.get('id')
    db = dbConnector()
    db.set_id(id)
    data = db.get_listing()
    return json.dumps(data,use_decimal=True)


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


@application.route('/amenities')
def amenities():
    """Returns listing amenities and missing amenities that the most popular listings offer"""
    id = request.args.get('id')
    db = dbConnector()
    helper = Helper()
    db.set_id(id)
    data = db.get_listing()
    zipcode = data[0]['zipcode']
    price = data[0]['price']
    listing_amenities = data[0]['amenities']
    total_amenities = db.get_amens_by_zip(zipcode)
    amens = helper.amens(listing_amenities, total_amenities,price)
    return json.dumps(amens, use_decimal=True)


@application.route('/percentiles')
def percentiles():
    id = request.args.get('id')
    filter = request.args.get('filter')
    db = dbConnector()
    helper = Helper()
    db.set_id(id)
    data = db.get_listing()
    zipcode = data[0]['zipcode']
    listing_price = data[0]['price']
    prices = db.get_price_by_zip(zipcode)
    preds = helper.percents(float(listing_price),prices)
    property_type = data[0]['property_type']
    data = db.get_percentile_totals(filter, zipcode, property_type)
    percentiles = [np.percentile(data, x) for x in range(10, 110, 10)]
    totals = helper.percentile_totals(percentiles,data)
    response = {'total_listings':totals,'filter':filter,'pricing_percentiles':preds}
    return json.dumps(response,use_decimal=True)



if __name__ == '__main__':
    app.run(debug=True)
