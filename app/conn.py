import mysql.connector

# Database configuration
db_config = {}


def db_conn_select(sql_to_execute):
    cursor = None
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql_to_execute)

        rows = cursor.fetchall()
        # for row in rows:
        #     print(row)
        return rows

    except mysql.connector.Error as err:
        print("Error:", err)
        return None

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def db_conn_insert(sql_to_execute):
    cursor = None
    connection = None
    try:
        print("db_conn_insert1")
        connection = mysql.connector.connect(**db_config)
        print("db_conn_insert1.1")
        cursor = connection.cursor()
        print("db_conn_insert1.2")
        print(sql_to_execute)
        cursor.execute(sql_to_execute)
        print("db_conn_insert2")

        rows = cursor.fetchone()
        connection.commit()
        print("db_conn_insert3")

        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("db_conn_insert4")
        return rows

    except mysql.connector.Error as err:
        print("Error:", err)
        return None

    finally:
        # Close the cursor and connection
        print("finally called --------------")
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def db_conn_delete(sql_to_execute):
    cursor = None
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(sql_to_execute)

        connection.commit()

        if cursor:
            cursor.close()
        if connection:
            connection.close()
        return None

    except mysql.connector.Error as err:
        print("Error:", err)
        return None

    finally:
        # Close the cursor and connection
        print("finally called delete--------------")
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def db_conn_update(sql_to_execute):
    cursor = None
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(sql_to_execute)

        connection.commit()

        if cursor:
            cursor.close()
        if connection:
            connection.close()
        return None

    except mysql.connector.Error as err:
        print("Error:", err)
        return None

    finally:
        # Close the cursor and connection
        print("finally called update--------------")
        if cursor:
            cursor.close()
        if connection:
            connection.close()
