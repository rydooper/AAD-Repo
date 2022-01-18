import mysql.connector


def test(username, password, name, role, restaurant):
    parameters = {'username' : username, 'password' : password, 'name' : name, 'role' : role, 'restaurant' : restaurant}


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
        query = "CREATE DATABASE fridge_db"
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


########################################################################################################################

########################################################################################################################

def select_username(username, password):
    fridge_db = connect_db()
    db_cursor = fridge_db.cursor()
    query = """
        SELECT name, role, restaurant FROM users
        WHERE username = %(username)s
        AND password = %(password)s
    """

    try:
        db_cursor.execute(query, {'username' : username, 'password' : password})
        fridge_db.commit()
    except mysql.connector.Error as error_msg:
        print(error_msg)

    db_cursor.close()
    fridge_db.close()


def insert_new_user(username, password, name, role, restaurant):
    fridge_db = connect_db()
    db_cursor = fridge_db.cursor()
    query = """
        INSERT INTO users (username, password, name, role, restaurant)
        VALUES (%(username)s, %(password)s, %(name)s, %(role)s, %(restaurant)s)
    """

    try:
        db_cursor.execute(query, {'username' : username, 'password' : password, 'name' : name, 'role' : role, 'restaurant' : restaurant})
        fridge_db.commit()
    except mysql.connector.Error as error_msg:
        print(error_msg)

    db_cursor.close()
    fridge_db.close()