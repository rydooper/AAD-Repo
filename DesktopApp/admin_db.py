import mysql.connector


########################################################################################################################
# Initial connection to MYSQL server and creation of fridge_db.
########################################################################################################################

def connect():
    try:
        fridge_db = mysql.connector.connect(user="fridgeAdmin",
                                            password="MontyFr1dge",
                                            host="mysql-azure-fridge-dr.mysql.database.azure.com",
                                            port=3306
                                            )

        # fridge_db = mysql.connector.connect(user="fridgeUser",
        #                                     password="fridgeUser",
        #                                     host="localhost",
        #                                     port=3306,
        #                                     auth_plugin='mysql_native_password'
        #                                     )
        return fridge_db
    except mysql.connector.Error as err:
        print(err)


def create_db():
    fridge_db = connect()
    db_cursor = fridge_db.cursor()

    try:
        query = "CREATE DATABASE IF NOT EXISTS fridge_db"
        db_cursor.execute(query)
        fridge_db.commit()
    except mysql.connector.Error as error_msg:
        print(error_msg)

    db_cursor.close()
    fridge_db.close()


########################################################################################################################
# Initial table creation.
########################################################################################################################

def create_users():
    create_users_query = """
        CREATE TABLE IF NOT EXISTS users (
        username VARCHAR(128),
        password VARCHAR(128),
        name VARCHAR(30),
        role VARCHAR(15), 
        restaurant VARCHAR(30),
        PRIMARY KEY (username)
        )
    """
    return create_table(create_users_query)


def create_items():
    create_items_query = """
        CREATE TABLE IF NOT EXISTS items (
        itemName VARCHAR(30), 
        expiry DATE, 
        stock INT, 
        weightPerItem INT,
        allergyInfo VARCHAR(100),
        recyclingInfo VARCHAR(100),
        PRIMARY KEY (itemName, expiry)
        )
    """
    return create_table(create_items_query)


def create_fridge_codes():
    create_fridge_codes_query = """
    CREATE TABLE  IF NOT EXISTS fridgeCodes (
    fridgeID VARCHAR(30),
    fridgeCode VARCHAR(128),
    PRIMARY KEY (fridgeID)
    )
    """
    return create_table(create_fridge_codes_query)


########################################################################################################################
# Connection to fridge_db, create_table SQL table builder and execute_sql query builder.
########################################################################################################################

def connect_db():
    try:
        fridge_db = mysql.connector.connect(user="fridgeAdmin",
                                            password="MontyFr1dge",
                                            host="mysql-azure-fridge-dr.mysql.database.azure.com",
                                            port=3306,
                                            database="fridge_db"
                                            )

        # fridge_db = mysql.connector.connect(user="fridgeUser",
        #                                     password="fridgeUser",
        #                                     host="localhost",
        #                                     port=3306,
        #                                     database="fridge_db",
        #                                     auth_plugin='mysql_native_password'
        #                                     )
        return fridge_db
    except mysql.connector.Error as err:
        print(err)


def create_table(query):
    fridge_db = connect_db()
    db_cursor = fridge_db.cursor()

    try:
        db_cursor.execute(query)
        fridge_db.commit()
    except mysql.connector.Error as error_msg:
        print(error_msg)

    db_cursor.close()
    fridge_db.close()
