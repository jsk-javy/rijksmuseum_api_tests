import sys
from pathlib import Path

# Append the root directory to sys.path
# This will adjust the import path so Python recognizes 'src' as a module
sys.path.append(str(Path(__file__).resolve().parents[2]))


import sqlite3
from src.configs.hosts_config import DB_PATH

class DatabaseUtility:
    def __init__(self, db_name=DB_PATH):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def fetch_collection_details(self, object_number):
        """Retrieve expected data from the database for a specific object number"""
        self.connect()

        query = """
        SELECT id, objectNumber, title, principalMakerName, hasImage, showImage 
        FROM CollectionDetails
        WHERE objectNumber = ?
        """
        
        self.cursor.execute(query, (object_number,))
        result = self.cursor.fetchone()
        self.close()

        if result:
            return {
                "id": result[0],
                "objectNumber": result[1],
                "title": result[2],
                "principalMakerName": result[3],
                "hasImage": bool(result[4]),
                "showImage": bool(result[5])
                }
        return None
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
