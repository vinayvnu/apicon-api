import mysql.connector

# Database configuration
db_config = {
    "host": "localhost",
    "port": 3308,
    "user": "root",
    "password": "password",
    "database": "BlazerexSql",
}

def db_conn():
    cursor = None
    connection = None
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)

        # Create a cursor
        cursor = connection.cursor()

        # Execute a sample query
        # cursor.execute("SELECT * FROM apicon.posts")

        # Fetch and print the results
        # rows = cursor.fetchall()
        # for row in rows:
        #     print(row)

    except mysql.connector.Error as err:
        print("Error:", err)
        return None

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return cursor




