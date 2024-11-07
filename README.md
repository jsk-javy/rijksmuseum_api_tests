
# Rijksmuseum API Testing Framework

This project is an automated testing framework designed for validating the Rijksmuseum API. It includes various tests to verify the retrieval and structure of art collection data and object details.

## Setup Instructions

# Prerequisites
  Python: Make sure Python 3.x is installed.

# Virtual Environment
  It’s recommended to create a virtual environment.
  python -m venv Virtual environment name

# Install Dependencies
   Use `pip install -r requirements.txt` to install necessary libraries.

## Setting up the Database
   The db_setup.py script creates a table and inserts initial data.

 # Run the Database Setup:
   Before executing the test case run Database setup file
   
   'python src/db_setup/db_setup.py'
   
   Verify Database Entries (optional): Check initial database entries by running:

## Running the Tests
   Run All Tests: To execute all tests with reports, use the following command:
   'pytest Tests --junitxml=report.xml'

# Individual Tests: Run a specific test file:
  pytest -s Tests/test_collection_details.py::TestCaseName

# Future Improvements
Enhanced Logging: Implement comprehensive logging across all modules.

Dynamic Object ID Retrieval: Automate the objectNumber update to handle API changes.

Complete Jenkins Pipeline: Finalize Jenkins integration for CI/CD.

Code Refactoring: Ensure modular code structure with further refactoring as needed.
