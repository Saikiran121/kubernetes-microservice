# Import Flask modules
from flask import Flask, request, render_template
from flask_mysqldb import MySQL
import os

# Create an object named app
app = Flask(__name__)

# Configure mysql database using environment variables
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'admin@123')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'test')
app.config['MYSQL_PORT'] = 3306
mysql = MySQL(app)

# Write a function named `init_phonebook_db` which initializes the phonebook db
def init_phonebook_db():
    with app.app_context():
        connection = mysql.connection
        cursor = connection.cursor()
        phonebook_table = """
        CREATE TABLE IF NOT EXISTS phonebook(
        id INT NOT NULL AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        number VARCHAR(100) NOT NULL,
        PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        cursor.execute(phonebook_table)
        connection.commit()
        cursor.close()

# Write a function named `insert_person` which inserts person into the phonebook table in the db,
# and returns text info about result of the operation
def insert_person(name, number):
    with app.app_context():
        connection = mysql.connection
        cursor = connection.cursor()
        query = "SELECT * FROM phonebook WHERE name = %s"
        cursor.execute(query, (name.strip().lower(),))
        row = cursor.fetchone()
        if row is not None:
            cursor.close()
            return f'Person with name {row[1].title()} already exists.'

        insert = "INSERT INTO phonebook (name, number) VALUES (%s, %s)"
        cursor.execute(insert, (name.strip().lower(), number))
        connection.commit()
        cursor.close()
        return f'Person {name.strip().title()} added to Phonebook successfully'

# Write a function named `update_person` which updates the person's record in the phonebook table,
# and returns text info about result of the operation
def update_person(name, number):
    with app.app_context():
        connection = mysql.connection
        cursor = connection.cursor()
        query = "SELECT * FROM phonebook WHERE name = %s"
        cursor.execute(query, (name.strip().lower(),))
        row = cursor.fetchone()
        if row is None:
            cursor.close()
            return f'Person with name {name.strip().title()} does not exist.'

        update = "UPDATE phonebook SET number = %s WHERE id = %s"
        cursor.execute(update, (number, row[0]))
        connection.commit()
        cursor.close()
        return f'Phone record of {name.strip().title()} is updated successfully'

# Write a function named `delete_person` which deletes person record from the phonebook table in the db,
# and returns text info about result of the operation
def delete_person(name):
    with app.app_context():
        connection = mysql.connection
        cursor = connection.cursor()
        query = "SELECT * FROM phonebook WHERE name = %s"
        cursor.execute(query, (name.strip().lower(),))
        row = cursor.fetchone()
        if row is None:
            cursor.close()
            return f'Person with name {name.strip().title()} does not exist, no need to delete.'

        delete = "DELETE FROM phonebook WHERE id = %s"
        cursor.execute(delete, (row[0],))
        connection.commit()
        cursor.close()
        return f'Phone record of {name.strip().title()} is deleted from the phonebook successfully'

# Define routes and view functions...
@app.route('/add', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        name = request.form['username']
        if not name or name.strip() == "":
            return render_template('add-update.html', not_valid=True, message='Invalid input: Name cannot be empty', show_result=False, action_name='save', developer_name='Devenes')
        elif name.isdecimal():
            return render_template('add-update.html', not_valid=True, message='Invalid input: Name of person should be text', show_result=False, action_name='save', developer_name='Devenes')

        phone_number = request.form['phonenumber']
        if not phone_number or phone_number.strip() == "":
            return render_template('add-update.html', not_valid=True, message='Invalid input: Phone number cannot be empty', show_result=False, action_name='save', developer_name='Devenes')
        elif not phone_number.isdecimal():
            return render_template('add-update.html', not_valid=True, message='Invalid input: Phone number should be in numeric format', show_result=False, action_name='save', developer_name='Devenes')

        result = insert_person(name, phone_number)
        return render_template('add-update.html', show_result=True, result=result, not_valid=False, action_name='save', developer_name='Devenes')
    else:
        return render_template('add-update.html', show_result=False, not_valid=False, action_name='save', developer_name='Devenes')

@app.route('/update', methods=['GET', 'POST'])
def update_record():
    if request.method == 'POST':
        name = request.form['username']
        if not name or name.strip() == "":
            return render_template('add-update.html', not_valid=True, message='Invalid input: Name cannot be empty', show_result=False, action_name='update', developer_name='Devenes')
        phone_number = request.form['phonenumber']
        if not phone_number or phone_number.strip() == "":
            return render_template('add-update.html', not_valid=True, message='Invalid input: Phone number cannot be empty', show_result=False, action_name='update', developer_name='Devenes')
        elif not phone_number.isdecimal():
            return render_template('add-update.html', not_valid=True, message='Invalid input: Phone number should be in numeric format', show_result=False, action_name='update', developer_name='Devenes')

        result = update_person(name, phone_number)
        return render_template('add-update.html', show_result=True, result=result, not_valid=False, action_name='update', developer_name='Devenes')
    else:
        return render_template('add-update.html', show_result=False, not_valid=False, action_name='update', developer_name='Devenes')

@app.route('/delete', methods=['GET', 'POST'])
def delete_record():
    if request.method == 'POST':
        name = request.form['username']
        if not name or name.strip() == "":
            return render_template('delete.html', not_valid=True, message='Invalid input: Name cannot be empty', show_result=False, developer_name='Devenes')
        result = delete_person(name)
        return render_template('delete.html', show_result=True, result=result, not_valid=False, developer_name='Devenes')
    else:
        return render_template('delete.html', show_result=False, not_valid=False, developer_name='Devenes')

@app.route('/', methods=['GET', 'POST'])
def find_records():
    return render_template('index.html', show_result=False, developer_name='Devenes')

# Add a statement to run the Flask application which can be reached from any host on port 80.
if __name__ == '__main__':
    init_phonebook_db()
    app.run(host='0.0.0.0', port=5000)

