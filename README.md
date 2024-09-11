# Zip Code API

This is a simple API that returns the city and state for a given zip code. The API is built using Python and Flask, and it reads zip code data from a CSV file hosted on GitHub.

## Features

- Retrieve city and state information for a given zip code
- CSV file with zip code data is hosted on GitHub for easy access and updates
- Deployed on Render for easy hosting and management

## API Endpoint

- `GET /api/zipcode/<zipcode>`
  - Retrieves the city and state for the specified `<zipcode>`
  - Returns a JSON response with the following structure:
    ```json
    {
      "city": "City Name",
      "state": "State Name"
      "state_id": "State ID"
      "timezone": "timezone"
    }
    ```
  - If the zip code is not found, returns a JSON response with an error message and a 404 status code:
    ```json
    {
      "error": "Zip code not found"
    }
    ```

## Technologies Used

- Python
- Flask
- Render (for hosting)
- GitHub (for storing the CSV file)
