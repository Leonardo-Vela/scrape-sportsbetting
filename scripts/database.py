import sqlite3
import pandas as pd


def write_to_db(df):
    if not df.empty:
        # Connect to the SQLite database
        connection = sqlite3.connect('test_database.db')
        cursor = connection.cursor()
        print("Connected to Database...")

        columns = df.columns
        
        column_str = ', '.join(columns)

        create_table_if_not_exists = f"CREATE TABLE IF NOT EXISTS matches({column_str})"
        cursor.execute(create_table_if_not_exists)

        # SQL insert template using placeholders for values
        placeholders = ', '.join(['?'] * len(columns))
        insert_query = f"INSERT INTO matches ({column_str}) VALUES ({placeholders})"

        # Loop through each row in the DataFrame and insert dynamically
        for _, row in df.iterrows():
            values = tuple(row[col] for col in columns)  # Extract values based on column names
            cursor.execute(insert_query, values)

        connection.commit()
        print("Wrote to Database...")
        print("--------------")
        connection.close()
    else:
        print("Nothing to store ...")
        print("--------------")