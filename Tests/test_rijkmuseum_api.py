import requests
import logging
import json
import time




API_BASE_URLS = "https://www.rijksmuseum.nl/api/en/collection"
API_KEY = "0fiuZFh4"

def test_retrieve_collection():
    response = requests.get(f"{API_BASE_URLS}", params={"key": API_KEY, "format": "json"})
    assert response.status_code == 200, "Expected status code is 200"
    data = response.json()
    assert "artObjects" in data, "response should contain 'artObjects'"
    assert len(data["artObjects"]) > 0, "length of 'artObjects' should not be empty."

def test_retrieve_object_details():
    "Retrieve an object to get a valid object ID"
    collection_response = requests.get(f"{API_BASE_URLS}", params={"key": API_KEY, "format": "json"})
    assert collection_response.status_code == 200
    data = collection_response.json()
    first_object_id = data["artObjects"][0]["objectNumber"]
    for artobject in data["artObjects"]:
        print(f"object id:{artobject['objectNumber']}")

    # Get details for that specific object
    details_response = requests.get(f"{API_BASE_URLS}/{first_object_id}", params={"key": API_KEY, "format": "json"})
    assert details_response.status_code == 200
    details_data = details_response.json()
    json_formatted_str = json.dumps(details_data, indent=0)
    print(json_formatted_str)
    assert "artObject" in details_data, "Expected 'artObjects' in object details"
    assert "id" in details_data["artObject"], "Expected 'title in object details"
    assert "title" in details_data["artObject"], "Expected 'title in object details"
    assert "principalOrFirstMaker" in details_data["artObject"], "Expectd 'principalOrFirstMaker' in object details"
    

def test_invalid_object_id():
    invalid_object_id = "invalid_11"
    response = requests.get(f"{API_BASE_URLS}/{invalid_object_id}", params={"key": API_KEY, "format": "json"})
    assert response.status_code == 200, "Expected status code 200 for invalid object ID"
    data = response.json()
    assert data.get('artObject') is None, "Expected artobject value to be null for invalid object ID"

def test_invalid_parameters():
    response = requests.get(f"{API_BASE_URLS}", params ={"key": API_KEY, "format": "json", "test": 2})
    print(response.status_code)
    data = response.json()
    print(json.dumps(data, indent=0))
    # assert response.status_code != 200, "Expected non 200 status code for invalid params"

def test_incorrect_api_key():
    invalid_api_key = "012wwed"
    response = requests.get(f"{API_BASE_URLS}", params={"key": invalid_api_key, "format": "json"})
    print(response.status_code)
    assert response.status_code == 401, "Expected non 200 status code for invalid api key"
    data = response.json()
    print(json.dumps(data, indent=0))


def test_api_performance():
    # Response time validation
    start_time = time.time()
    response = requests.get(f"{API_BASE_URLS}", params= {"key": API_KEY, "format": "json"})
    response_time = time.time() - start_time
    assert response_time < 0.5, f"Response took too long: {response_time} sec."


def test_high_volume_api():
    # High number of requests in a short period
    for _ in range(100):
        response = requests.get(f"{API_BASE_URLS}", params={"key": API_KEY, "format": "json"})
        if response.status_code == 429:
            print("Rate limit exceed")
            break

