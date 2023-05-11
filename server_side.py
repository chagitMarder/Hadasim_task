import calendar
import datetime
import os

import matplotlib.pyplot as plt

from flask import Flask, jsonify, request, send_file
import sqlite3
from corona_DB import create_member_table, create_vaccine_details_table

app = Flask(__name__)


def get_DB():
    conn = sqlite3.connect('corona_DB.db')
    return conn


def close_DB(conn):
    conn.close()


@app.route('/api/get_all_members', methods=['GET'])
def get_all_members():
    my_database = get_DB()
    my_cursor = my_database.cursor()
    query = '''
    SELECT * FROM members
    '''
    my_cursor.execute(query)
    my_database.commit()
    result = my_cursor.fetchall()
    return jsonify(result)


@app.route('/api/get_member_by_id/<int:id>', methods=['GET'])
def get_members_by_id(id):
    my_database = get_DB()
    my_cursor = my_database.cursor()
    query = f'''SELECT * FROM members
        WHERE members.id = {id}'''
    my_cursor.execute(query)
    my_database.commit()
    result = my_cursor.fetchall()
    return jsonify(result)


@app.route('/api/get_member_and_values_by_id/<int:id>', methods=['GET'])
def get_members_and_values_by_id(id):
    my_database = get_DB()
    my_cursor = my_database.cursor()
    query = f'''SELECT * FROM members
        JOIN vaccine_details ON members.id = vaccine_details.id
        WHERE members.id = {id}'''
    my_cursor.execute(query)
    my_database.commit()
    result = my_cursor.fetchall()
    return jsonify(result)


def member_validation_checks(new_member):
    if not new_member.get('id'):
        return {'error': 'Member ID is required'}
    elif len(str(new_member.get('id'))) != 9:
        return {'error': 'Not a valid member ID'}
    elif not new_member.get('first_name'):
        return {'error': 'First name is required'}
    elif not new_member.get('last_name'):
        return {'error': 'Last name is required'}
    else:
        my_database = get_DB()
        my_cursor = my_database.cursor()
        query = f"SELECT COUNT(*) FROM members WHERE id = '{new_member.get('id')}'"
        my_cursor.execute(query)
        count = my_cursor.fetchone()[0]
        if count > 0:
            return {'error': 'Member ID already exists'}
        else:
            return None


@app.route('/insert_member', methods=['POST'])
def insert_member():
    new_member = request.json
    validation_result = member_validation_checks(new_member)
    if validation_result:
        return jsonify(validation_result)
    my_database = get_DB()
    my_cursor = my_database.cursor()

    query = '''INSERT INTO members
                        (id, first_name, last_name, city, street, number, birth_date, phone, self_phone)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    my_cursor.execute(query, (
    new_member['id'], new_member['first_name'], new_member['last_name'], new_member['city'], new_member['street'],
    new_member['number'], new_member['birth_date'], new_member['phone'], new_member['self_phone']))
    my_database.commit()
    answer = {'status': 'success'}
    return jsonify(answer)


def value_validation_checks(new_member):
    my_database = get_DB()
    my_cursor = my_database.cursor()
    if not new_member.get('id'):
        return {'error': 'Member ID is required'}
    elif len(str(new_member.get('id'))) != 9:
        return {'error': 'Not a valid member ID'}
    elif new_member.get('sick_date') is None and new_member.get('recover_date') is not None:
        return {'error': 'you can not add recover date without sick date'}
    elif new_member.get('sick_date') is not None and new_member.get('recover_date') is not None and new_member.get(
            'sick_date') >= new_member.get('recover_date'):
        return {'error': 'recover date can not be before sick date'}
    query = f"SELECT COUNT(*) FROM vaccine_details WHERE id = '{new_member.get('id')}'"
    my_cursor.execute(query)
    count = my_cursor.fetchone()[0]
    if count > 0:
        return {'error': 'Member ID already exists'}
    query1 = f"SELECT COUNT(*) FROM members WHERE id = '{new_member.get('id')}'"
    my_cursor.execute(query1)
    count = my_cursor.fetchone()[0]
    if count == 0:
        return {'error': 'This ID is not a member'}
    return None


@app.route('/insert_value', methods=['POST'])
def insert_value():
    new_member = request.json
    validation_result = value_validation_checks(new_member)
    if validation_result:
        return jsonify(validation_result)
    my_database = get_DB()
    my_cursor = my_database.cursor()

    query = '''INSERT INTO vaccine_details
                        (id, first_date, first_manufacturer, second_date, second_manufacturer, 
                        third_date, third_manufacturer, fourth_date, fourth_manufacturer, sick_date, recover_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    my_cursor.execute(query, (
    new_member['id'], new_member['first_date'], new_member['first_manufacturer'], new_member['second_date'],
    new_member['second_manufacturer'],
    new_member['third_date'], new_member['third_manufacturer'],
    new_member['fourth_date'], new_member['fourth_manufacturer'], new_member['sick_date'], new_member['recover_date']))
    my_database.commit()
    answer = {'status': 'success'}
    return jsonify(answer)


def plot_graph(result):
    # Plot the graph
    plt.plot(result.keys(), result.values())
    plt.xlabel('Date')
    plt.ylabel('Number of sick members')
    plt.title('Sick Members Last Month')
    plt.xticks(rotation=90)
    filename = 'sick_members_last_month.png'
    if not os.path.exists(filename):
        plt.savefig(filename)
    plt.show()


@app.route('/api/sick_members_last_month', methods=['GET'])
def get_sick_members_last_month():
    my_database = get_DB()
    my_cursor = my_database.cursor()
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    num_of_days_in_month = calendar.monthrange(current_year, current_month)[1]
    start_date = datetime.date.today() - datetime.timedelta(days=num_of_days_in_month)
    result = {}
    for i in range(num_of_days_in_month):
        day = start_date + datetime.timedelta(days=i)
        query = f'''
            SELECT COUNT(*) 
            FROM vaccine_details 
            WHERE sick_date <= '{day}'
        '''
        my_cursor.execute(query)
        num_of_sick_members = my_cursor.fetchone()[0]
        query = f'''
            SELECT COUNT(*) 
            FROM vaccine_details 
            WHERE recover_date <= '{day}'
        '''
        my_cursor.execute(query)
        num_of_recover_members = my_cursor.fetchone()[0]
        result[str(day)] = num_of_sick_members - num_of_recover_members
    my_database.commit()
    plot_graph(result)
    return send_file('sick_members_last_month.png', mimetype='image/png')



@app.route('/api/not_vaccined_members', methods=['GET'])
def get_not_vaccined_members():
    my_database = get_DB()
    my_cursor = my_database.cursor()
    query = f'''SELECT count(*)
            FROM vaccine_details
            WHERE vaccine_details.first_date IS NULL and vaccine_details.second_date IS NULL
            and vaccine_details.third_date IS NULL and vaccine_details.fourth_date IS NULL'''
    my_cursor.execute(query)
    my_database.commit()
    result = my_cursor.fetchall()
    return jsonify(result)


if __name__ == '__main__':
    create_member_table()
    create_vaccine_details_table()
    app.run(debug=True)
