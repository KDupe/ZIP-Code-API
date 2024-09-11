import csv
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Read zip code data from CSV file on GitHub
url = 'https://raw.githubusercontent.com/KDupe/ZIP-Code-API/blob/main/US%20Zip%20Codes.csv'
response = requests.get(url)
csv_data = response.text


# Read zip code data from CSV file
zip_data = {}
with open('Y:/US Zip Codes/US Zip Codes.csv', 'r') as file:
    reader = csv.DictReader(file)
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
    app.run()
