import sys
from pathlib import Path

# Append the root directory to sys.path
# This will adjust the import path so Python recognizes 'src' as a module
sys.path.append(str(Path(__file__).resolve().parents[2]))

import requests
from src.configs import hosts_config as config


class RequestUtility:
    def __init__(self, base_url = None):
        self.base_url = config.API_BASE_URLS
        self.api_key = config.API_KEY


    def _make_request(self, method, endpoint, **kwargs):
        """Helper method to handle http request"""

        url = f"{self.base_url}{endpoint}"
        # Set default headers
        headers = kwargs.pop("headers", {}) or {}
        headers["Authorization"] = f"Bearer {self.api_key}"
        try:
            # Perform the HTTP request
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()  # Raises HTTPError if the response was unsuccessful
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
       
        return None
    
    def get(self, endpoint, params=None, headers=None):
        """Handles GET requests."""
        return self._make_request("GET", endpoint, params=params, headers=headers)

    def post(self, endpoint, data=None, json=None, headers=None):
        """Handles POST requests."""
        return self._make_request("POST", endpoint, data=data, json=json, headers=headers)
    
    def fetch_api_data(self, object_number):
        """Fetch data from the Rijksmuseum API for a specific object ID."""
        endpoint = f"/{object_number}"
        params = {"key": self.api_key, "format": "json"}

        data = self.get(endpoint, params=params)
        art_object = data.get("artObject", {}) if data else None
        # Check if data is empty and handle accordingly
        if not art_object:
            raise ValueError(f"No 'artObject' data found for object_id:{object_number}")

        return {

            "id": art_object.get("id"),
            "objectNumber": art_object.get("objectNumber"),
            "title": art_object.get("title"),
            "principalMakerName": art_object.get("principalMakers", [{}])[0].get("name"),
            "hasImage": art_object.get("hasImage"),
            "showImage": art_object.get("showImage")
        }
    
    def retrieve_object_details(self):
        "Retrieve an object to get a valid object ID"
        data = self.get(endpoint="", params={"key": self.api_key, "format": "json"})
        if data is None:
            print("Failed to retrieve data.")
            return
        art_objects = data.get("artObjects", [])
        for artobject in art_objects:
            print(f"object Number:{artobject['objectNumber']}")
            print(f"object id:{artobject['id']}")

# To obtain object Number and object id
obj_request = RequestUtility()
obj_request.retrieve_object_details()