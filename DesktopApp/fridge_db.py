import mysql.connector


########################################################################################################################
# Database function to be called from main program.
########################################################################################################################

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
        SELECT 
        itemName, DATE_FORMAT(expiry, "%d %M %Y"), stock, 
        weightPerItem, allergyInfo, recyclingInfo 
        FROM items
        ORDER BY expiry ASC, itemName ASC
    """
    return execute_sql(select_items_query, (), True)


def add_items(item_name, expiry, quantity, weight_per_item, allergy_info, recycling_info):
    insert_items_query = """
        INSERT INTO items (itemName, expiry, stock, weightPerItem, allergyInfo, recyclingInfo)
        VALUES (%(item_name)s, %(expiry)s, %(quantity)s, %(weight_per_item)s, %(allergy_info)s, %(recycling_info)s)
        ON DUPLICATE KEY UPDATE stock = stock + %(quantity)s
    """
    insert_items_values = {'item_name': item_name, 'expiry': expiry, 'quantity': quantity,
                           'weight_per_item': weight_per_item, 'allergy_info' : allergy_info,
                           'recycling_info' : recycling_info }
    return execute_sql(insert_items_query, insert_items_values)


def remove_items(item_name, expiry, quantity):
    remove_items_query = """
    UPDATE items 
    SET stock = stock - %(quantity)s
    WHERE itemName = %(item_name)s
    AND expiry = %(expiry)s
    """
    remove_items_values = {'item_name' : item_name, 'expiry' : expiry, 'quantity' : quantity}
    message = execute_sql(remove_items_query, remove_items_values)
    if check_stock(item_name, expiry) <= 0:
        delete_record(item_name, expiry)
    return message


########################################################################################################################
# Auxiliary functions for remove_items
########################################################################################################################

def check_stock(item_name, expiry):
    check_stock_query = """
    SELECT stock FROM items
    WHERE itemName = %(item_name)s
    AND expiry = %(expiry)s
    """
    check_stock_values = {'item_name' : item_name, 'expiry' : expiry}
    stock = execute_sql(check_stock_query, check_stock_values, True)
    if not stock:
        print("Item does not exist in DB.")
        return 1
    return int(stock[0][0])


def delete_record(item_name, expiry):
    delete_record_query = """
    DELETE FROM items
    WHERE itemName = %(item_name)s
    AND expiry = %(expiry)s
    """
    delete_record_values = {'item_name' : item_name, 'expiry' : expiry}
    return execute_sql(delete_record_query, delete_record_values)


########################################################################################################################
# Connection to fridge_db, create_table SQL table builder and execute_sql query builder.
########################################################################################################################

def connect_db():
    try:
        # fridge_db = mysql.connector.connect(user="fridgeUser",
        #                                     password="fridgeUser",
        #                                     host="mysql-azure-fridge-dr.mysql.database.azure.com",
        #                                     port=3306,
        #                                     database="fridge_db",
        #                                     ssl_ca="DigiCertGlobalRootCA.crt.pem",
        #                                     )

        fridge_db = mysql.connector.connect(user="fridgeUser",
                                            password="fridgeUser",
                                            host="localhost",
                                            port=3306,
                                            database="fridge_db",
                                            auth_plugin='mysql_native_password'
                                            )
        return fridge_db
    except mysql.connector.Error as err:
        print(err)


def execute_sql(query, values, retrieve_results=False):
    sql_result = "Successful query."
    fridge_db = connect_db()
    db_cursor = fridge_db.cursor()

    try:
        db_cursor.execute(query, values)
        if retrieve_results:
            sql_result = db_cursor.fetchall()
        fridge_db.commit()
    except mysql.connector.Error as error_msg:
        print(error_msg)
        sql_result = "Unsuccessful query."

    db_cursor.close()
    fridge_db.close()
    return sql_result
