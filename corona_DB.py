import sqlite3
from datetime import date



def create_member_table():
    # connect to the database
    conn = sqlite3.connect('corona_DB.db')
    conn.text_factory = bytes;

    # create a cursor object
    my_cursor = conn.cursor()
    try:
        # create a table
        conn.execute('''CREATE TABLE IF NOT EXISTS members (
                        id INTEGER PRIMARY KEY,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        city TEXT,
                        street TEXT,
                        number INTEGER,
                        birth_date DATE,
                        phone TEXT,
                        self_phone TEXT
                    )''')

        # commit the changes
        conn.commit()

        # close the connection
        conn.close()
    except:
        print("unable to create the members table")
        conn.close()


def create_vaccine_details_table():
    # connect to the database
    conn = sqlite3.connect('corona_DB.db')
    conn.text_factory = bytes;

    # create a cursor object
    my_cursor = conn.cursor()
    try:
        # create a table
        conn.execute('''CREATE TABLE IF NOT EXISTS vaccine_details (
                        id INTEGER PRIMARY KEY,
                        first_date DATE,
                        first_manufacturer TEXT,
                        second_date DATE,
                        second_manufacturer TEXT,
                        third_date DATE,
                        third_manufacturer TEXT,
                        fourth_date DATE,
                        fourth_manufacturer TEXT,
                        sick_date DATE,
                        recover_date DATE
                    )''')

        # commit the changes
        conn.commit()

        # close the connection
        conn.close()
    except:
        print("unable to create the details table")
        conn.close()


