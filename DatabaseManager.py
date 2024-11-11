import sqlite3

def create_database(db_name='malware_hashes.db'):
    """Create a SQLite database and a table for storing malware hashes."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Create a table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hashes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                simple_hash TEXT NOT NULL,
                file_name TEXT NOT NULL,
                rolling_hashes TEXT,      -- Rolling hashes
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        print(f"Database '{db_name}' created and ready.")
    except sqlite3.Error as e:
        print(f"An error occurred while creating the database: {e}")
    finally:
        conn.close()

def insert_hash(simple_hash, file_name, rolling_hashes, db_name='malware_hashes.db'):
    """Insert a new hash entry into the database."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Convert the list of rolling hashes to a string
        rolling_hashes_str = ','.join(rolling_hashes)

        cursor.execute('''
            INSERT INTO hashes (simple_hash, file_name, rolling_hashes)
            VALUES (?, ?, ?)
        ''', (simple_hash, file_name, rolling_hashes_str))

        conn.commit()
        print(f"Hash for '{file_name}' inserted into the database.")
    except sqlite3.Error as e:
        print(f"An error occurred while inserting hash for '{file_name}': {e}")
    finally:
        conn.close()

def check_simple_hash(simple_hash, db_name='malware_hashes.db'):
    """Check if a simple hash is present in the database and return its details."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM hashes WHERE simple_hash = ?', (simple_hash,))
        row = cursor.fetchone()

        return row  # Return the row if found, otherwise None
    except sqlite3.Error as e:
        print(f"An error occurred while checking the hash: {e}")
        return None
    finally:
        conn.close()

def get_all_hashes(db_name='malware_hashes.db'):
    """Retrieve all rows from the database."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM hashes')
        rows = cursor.fetchall()

        return rows  # Return all rows
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving all hashes: {e}")
        return []
    finally:
        conn.close()

def get_hashes_by_file_name(file_name, db_name='malware_hashes.db'):
    """Retrieve rows based on a specific file name."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM hashes WHERE file_name = ?', (file_name,))
        rows = cursor.fetchall()

        return rows  # Return the rows that match the file name
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving hashes for '{file_name}': {e}")
        return []
    finally:
        conn.close()
