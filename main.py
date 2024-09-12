import csv
import requests
from flask import Flask, jsonify
from io import StringIO
import os

app = Flask(__name__)

# Read zip code data from CSV file on GitHub
url = 'https://raw.githubusercontent.com/KDupe/ZIP-Code-API/main/US%20Zip%20Codes.csv'
response = requests.get(url)
csv_data = response.text

# Read zip code data from CSV file
zip_data = {}
reader = csv.DictReader(StringIO(csv_data))
for row in reader:
    zipcode = row['zip']
    city = row['city']
    state = row['state_name']
    state_id = row['state_id']
    timezone = row['timezone']
    zip_data[zipcode] = {'city': city, 'state': state, 'state_id': state_id, 'timezone': timezone}

@app.route('/api/zipcode/<string:zipcode>', methods=['GET'])
def get_location(zipcode):
    if zipcode in zip_data:
        return jsonify(zip_data[zipcode])
    else:
        return jsonify({"error": "Zip code not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
