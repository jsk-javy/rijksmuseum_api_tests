import sqlite3
import sys
from pathlib import Path


# Append the root directory to sys.path
# This will adjust the import path so Python recognizes 'src' as a module
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.utilities.database_util import DatabaseUtility

db_util = DatabaseUtility()


def setup_database():
    """Create table and insert dummy data"""

    db_util.connect()


    db_util.cursor.execute("""
               CREATE TABLE IF NOT EXISTS CollectionDetails 
               (
               id TEXT PRIMARY KEY,
               objectNumber TEXT NOT NULL,
               title TEXT,
               principalMakerName TEXT,
               hasImage BOOLEAN,
               showImage BOOLEAN
               )
        """)
    

    # Dummy data to insert
    data_entries = [
        ('nl-SK-C-5', 'SK-A-447', 'De Nachtwacht', 'Rembrandt van Rijn', True, True),
        ('nl-SK-A-5', 'SK-A-1718', 'Het Melkmeisje', 'Johannes Vermeer', True, True),
        ('nl-SK-D-2', 'SK-A-3584', 'Zelfportret', 'Vincent van Gogh', True, True)
    ]

    db_util.cursor.executemany("""
            INSERT OR REPLACE INTO CollectionDetails (id, objectNumber, title, principalMakerName, hasImage, showImage)
            VALUES (?, ?, ?, ?, ?, ?)
            """, data_entries)

    db_util.conn.commit()

    print("Database setup and sample data has been added.")

    db_util.close()

def verify_database_entries():
    # Re-open the connection to read data
    db_util.connect()
    cursor = db_util.conn.cursor()

    # Query the data
    cursor.execute("SELECT * FROM CollectionDetails")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    db_util.close()


if __name__ == "__main__":
    setup_database()
    verify_database_entries()