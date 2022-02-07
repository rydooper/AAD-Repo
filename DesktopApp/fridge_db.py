import mysql.connector


# For querying the database, use the first 5 functions below. The parameters should be strings, for 'expiry' the format
# of the string must be "YYYY-MM-DD". By default, the functions will return a string to indicate a successful query or
# an unsuccessful query. If the query is a SELECT where you're expecting the database to return a row or many rows, then
# the function will return a list of tuples with each tuple containing data from one record.

# For example login will return a list containing one tuple, made up of name, role and restaurant.
# display_fridge_contents will return a list of tuples with each tuple containing data for one type of item in the db.
########################################################################################################################
# Database function to be called from main program.
########################################################################################################################

def signup(username, password, name, role, restaurant):
    insert_user_query = """
        INSERT INTO users (username, password, name, role, restaurant)
        VALUES (%(username)s, %(password)s, %(name)s, %(role)s, %(restaurant)s)
    """
    insert_user_values = {'username': username, 'password': password, 'name': name, 'role': role,
                          'restaurant': restaurant}
    return execute_sql(insert_user_query, insert_user_values)


def update_user(username):
    update_user_query = """
    UPDATE users
    SET role = %(role)
    WHERE username = %(username)s
    """
    update_user_values = {'username': username}
    return execute_sql(update_user_query, update_user_values)


def remove_user(username):
    remove_user_query = """
    DELETE FROM users
    WHERE username = %(username)s
    """
    remove_user_values = {'username': username}
    return execute_sql(remove_user_query, remove_user_values)


def login(username, password) -> list[tuple[str, str, str]]:
    select_user_details_query = """
        SELECT name, role, restaurant FROM users
        WHERE username = %(username)s
        AND password = %(password)s
    """
    select_user_details_values = {'username': username, 'password': password}
    user_details = execute_sql(select_user_details_query, select_user_details_values, True)
    return user_details if user_details else "Incorrect login details provided."


def display_fridge_contents() -> list[tuple]:
    select_items_query = """
        SELECT 
        itemName, stock, DATE_FORMAT(expiry, "%d %M %Y"),
        weightPerItem, allergyInfo, recyclingInfo 
        FROM items
        ORDER BY itemName ASC, expiry ASC
    """
    return execute_sql(select_items_query, (), True)


def display_item_alerts() -> list[tuple]:
    select_item_alerts_query = """
        SELECT 
        itemName, stock, DATE_FORMAT(expiry, "%d %M %Y"),
        weightPerItem, allergyInfo, recyclingInfo 
        FROM items
        WHERE (SELECT DATEDIFF(expiry, current_date()) AS DateDiff) < 4
        ORDER BY itemName ASC, expiry ASC
    """
    return execute_sql(select_item_alerts_query, (), True)


def generate_health_report() -> list[tuple]:
    generate_health_report_query = """
            SELECT 
            itemName, stock, DATE_FORMAT(expiry, "%d %M %Y"),
            weightPerItem, allergyInfo, recyclingInfo 
            FROM items
            WHERE (SELECT DATEDIFF(expiry, current_date()) AS DateDiff) <= 0
            ORDER BY itemName ASC, expiry ASC
        """
    return execute_sql(generate_health_report_query, (), True)


def display_users() -> list[tuple]:
    display_users_query = """
    SELECT
    username, name, role, restaurant
    FROM users
    ORDER BY name ASC
    """
    return execute_sql(display_users_query, (), True)


def add_items(item_name, expiry, quantity, weight_per_item, allergy_info, recycling_info):
    insert_items_query = """
        INSERT INTO items (itemName, expiry, stock, weightPerItem, allergyInfo, recyclingInfo)
        VALUES (%(item_name)s, %(expiry)s, %(quantity)s, %(weight_per_item)s, %(allergy_info)s, %(recycling_info)s)
        ON DUPLICATE KEY UPDATE stock = stock + %(quantity)s
    """
    insert_items_values = {'item_name': item_name, 'expiry': expiry, 'quantity': quantity,
                           'weight_per_item': weight_per_item, 'allergy_info': allergy_info,
                           'recycling_info': recycling_info}
    return execute_sql(insert_items_query, insert_items_values)


def remove_items(item_name, expiry, quantity):
    remove_items_query = """
    UPDATE items 
    SET stock = stock - %(quantity)s
    WHERE itemName = %(item_name)s
    AND expiry = %(expiry)s
    """
    remove_items_values = {'item_name': item_name, 'expiry': expiry, 'quantity': quantity}
    message = execute_sql(remove_items_query, remove_items_values)
    if check_stock(item_name, expiry) <= 0:
        delete_record(item_name, expiry)
    return message


########################################################################################################################
# Auxiliary functions for remove_items
########################################################################################################################

def check_stock(item_name, expiry) -> int:
    check_stock_query = """
    SELECT stock FROM items
    WHERE itemName = %(item_name)s
    AND expiry = %(expiry)s
    """
    check_stock_values = {'item_name': item_name, 'expiry': expiry}
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
    delete_record_values = {'item_name': item_name, 'expiry': expiry}
    return execute_sql(delete_record_query, delete_record_values)


########################################################################################################################
# Connection to fridge_db, create_table SQL table builder and execute_sql query builder.
########################################################################################################################

def connect_db():
    try:
        fridge_db = mysql.connector.connect(user="fridgeUser",
                                            password="fridgeUser",
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
