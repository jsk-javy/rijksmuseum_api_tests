import pytest
from src.utilities.database_util import DatabaseUtility
from src.utilities.request_utilities import RequestUtility
from src.configs.hosts_config import API_BASE_URLS, API_KEY, DB_PATH


# Initialize utility classes
db_util = DatabaseUtility()
request_util = RequestUtility()

@pytest.mark.parametrize("object_number", ["SK-C-1367, SK-A-4050,  SK-A-4691"]) 
def test_collection_details(object_number):
    """Test the collection details API against the expected database values."""
    expected_data = db_util.fetch_collection_details(object_number)
    if not expected_data:
        print(f"No expected data found in the DB for object id:{object_number}")
        return
    
    api_data = request_util.fetch_api_data(object_number)
    print(f"\n Testing object ID:{object_number}")
    for key, expected_value in expected_data.items():
        actual_value = api_data.get(key)
        if actual_value == expected_value:
            print(f"Test Passed: {key} matches the expected value.")
        else:
            print(f"Test Failed: {key} - Expected: {expected_value}, Got: {actual_value}")


def test_retrieve_collection():
    """Test to retrieve a collection and validate the response structure and content."""
    response_data = request_util.get(endpoint="", params={"key": API_KEY, "format": "json"})
    assert response_data is not None, "Expected non-empty response data"
    assert "artObjects" in response_data, "Response should contain 'artObjects'"
    assert len(response_data["artObjects"]) > 0, "Length of 'artObjects' should not be empty."
