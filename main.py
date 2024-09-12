import csv
import requests
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from io import StringIO
import os

app = Flask(__name__)

# Configure caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Configure rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)


# Read zip code data from CSV file on GitHub
@cache.cached(timeout=3600)  # Cache for 1 hour
def load_zip_data():
    url = 'https://raw.githubusercontent.com/KDupe/ZIP-Code-API/main/US%20Zip%20Codes.csv'
    response = requests.get(url)
    csv_data = response.text

    zip_data = {}
    reader = csv.DictReader(StringIO(csv_data))
    for row in reader:
        zipcode = row['zip']
        city = row['city']
        state = row['state_name']
        state_id = row['state_id']
        timezone = row['timezone']
        zip_data[zipcode] = {'city': city, 'state': state, 'state_id': state_id, 'timezone': timezone}

    return zip_data


@app.route('/api/zipcode/<string:zipcode>', methods=['GET'])
@limiter.limit("60 per minute")  # Specific rate limit for this endpoint
@cache.cached(timeout=300)  # Cache results for 5 minutes
def get_location(zipcode):
    zip_data = load_zip_data()
    if zipcode in zip_data:
        return jsonify(zip_data[zipcode])
    else:
        return jsonify({"error": "Zip code not found"}), 404


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
