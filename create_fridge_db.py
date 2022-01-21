import mysql.connector


def create_users():
    create_users_query = """
        CREATE TABLE IF NOT EXISTS users (
        username VARCHAR(30),
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


def signup(username, password, name, role, restaurant):
    insert_user_query = """
        INSERT INTO users (username, password, name, role, restaurant)
        VALUES (%(username)s, %(password)s, %(name)s, %(role)s, %(restaurant)s)
    """
    insert_user_values = {'username': username, 'password': password, 'name': name, 'role': role,
                          'restaurant' : restaurant}
    return execute_sql(insert_user_query, insert_user_values)


def login(username, password):
    select_user_details_query = """
        SELECT name, role, restaurant FROM users
        WHERE username = %(username)s
        AND password = %(password)s
    """
    select_user_details_values = {'username': username, 'password': password}
    user_details = execute_sql(select_user_details_query, select_user_details_values, True)
    if not user_details:
        return "Incorrect login details provided."
    return user_details


def display_fridge_contents():
    select_items_query = """
        SELECT * FROM items
        ORDER BY expiry ASC, itemName ASC
    """


def add_new_item(item_name, expiry, quantity, weight_per_item, allergy_info, recycling_info):
    insert_items_query = """
        INSERT INTO items (itemName, expiry, stock, weightPerItem, allergyInfo, recyclingInfo)
        VALUES (%(item_name)s, %(expiry)s, %(quantity)s, %(weight_per_item)s, %(allergy_info)s, %(recycling_info)s)
    """
    insert_items_values = {'item_name': item_name, 'expiry': expiry, 'quantity': quantity,
                           'weight_per_item': weight_per_item, 'allergy_info' : allergy_info,
                           'recycling_info' : recycling_info }
    return execute_sql(insert_items_query, insert_items_values)


def update_existing_item(item_name, expiry, new_quantity):
    update_items_query = """
        UPDATE items SET stock = %(new_quantity)s
        WHERE itemName = %(item_name)s
        AND expiry = %(expiry)s
    """
    update_items_values = {'item_name' : item_name, 'expiry' : expiry, 'new_quantity' : new_quantity}


########################################################################################################################

########################################################################################################################

def connect():
    try:
        fridge_db = mysql.connector.connect(user="fridgeAdmin",
                                            password="MontyFr1dge",
                                            host="mysql-azure-fridge-dr.mysql.database.azure.com",
                                            port=3306,
                                            ssl_ca="DigiCertGlobalRootCA.crt.pem",
                                            ssl_disabled=False)
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

########################################################################################################################

def connect_db():
    try:
        fridge_db = mysql.connector.connect(user="fridgeAdmin",
                                            password="MontyFr1dge",
                                            host="mysql-azure-fridge-dr.mysql.database.azure.com",
                                            port=3306,
                                            database="fridge_db",
                                            ssl_ca="DigiCertGlobalRootCA.crt.pem",
                                            ssl_disabled=False)
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


def execute_sql(query, values, display_results=False):
    sql_result = "Successful query."
    fridge_db = connect_db()
    db_cursor = fridge_db.cursor()

    try:
        db_cursor.execute(query, values)
        if display_results:
            sql_result = db_cursor.fetchall()
        fridge_db.commit()
    except mysql.connector.Error as error_msg:
        print(error_msg)
        sql_result = "Unsuccessful query."

    db_cursor.close()
    fridge_db.close()
    return sql_result
