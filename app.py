from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)



@app.route('/main')
def main():
    car_images = [
        url_for('static', filename='PIC/CAR/car1.jpg'),
        url_for('static', filename='PIC/CAR/car2.jpg'),
        url_for('static', filename='PIC/CAR/car3.jpg'),
        url_for('static', filename='PIC/CAR/car4.jpg'),
        url_for('static', filename='PIC/CAR/car5.jpg'),
        url_for('static', filename='PIC/CAR/car6.jpg'),
        url_for('static', filename='PIC/CAR/car7.jpg'),
        url_for('static', filename='PIC/CAR/car8.jpg'),
        url_for('static', filename='PIC/CAR/car9.jpg'),
        url_for('static', filename='PIC/CAR/car10.jpg'),
        url_for('static', filename='PIC/CAR/car11.jpg'),
        url_for('static', filename='PIC/CAR/car12.jpg'),
        # Add more image URLs as needed
    ]
    return render_template("main.html", car_images=car_images)


def create_car_table():
    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS car (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_name TEXT,
            year INTEGER,
            score INTEGER
        )
    ''')
    con.commit()
    con.close()

@app.route('/view', methods=['GET', 'POST'])
def view_cars():
    create_car_table()

    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()

    if request.method == 'POST':
        search_term = request.form.get('search_term')
        query = "SELECT * FROM car WHERE car_name LIKE ?"
        cur.execute(query, ('%' + search_term + '%',))
    else:
        cur.execute("SELECT * FROM car")

    sqlite_cars = cur.fetchall()
    con.close()

    return render_template("view.html", sqlite_cars=sqlite_cars)

@app.route('/delete/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()
    cur.execute("DELETE FROM car WHERE id=?", (car_id,))
    con.commit()
    con.close()
    return redirect(url_for('view_cars'))

@app.route('/update/<int:car_id>', methods=['POST'])
def update_car(car_id):
    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()

    new_car_name = request.form.get('new_car_name')
    new_year = request.form.get('new_year')
    new_score = request.form.get('new_score')

    # Validate that at least one field is filled out
    if not new_car_name and not new_year and not new_score:
        return "At least one field (New Car Name, New Year, or New Score) is required. Please go back and fill it out."

    # Update only the fields that are provided
    if new_car_name:
        cur.execute("UPDATE car SET car_name=? WHERE id=?", (new_car_name, car_id))
    if new_year:
        cur.execute("UPDATE car SET year=? WHERE id=?", (new_year, car_id))
    if new_score:
        cur.execute("UPDATE car SET score=? WHERE id=?", (new_score, car_id))

    con.commit()
    con.close()

    return redirect(url_for('view_cars'))

@app.route('/addCar', methods=['GET', 'POST'])
def add_car():
    create_car_table()

    if request.method == 'POST':
        car_name = request.form.get('car_name')
        year = request.form.get('year')
        score = request.form.get('score')

        if not car_name or not year or not score:
            return "All fields are required. Please go back and fill them out."

        con = sqlite3.connect("tutorial.db")
        cur = con.cursor()
        cur.execute('''
            INSERT INTO car (car_name, year, score)
            VALUES (?, ?, ?)
        ''', (car_name, year, score))
        con.commit()
        con.close()

    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM car")
    cars = cur.fetchall()
    con.close()

    return render_template("addCar.html", cars=cars)

@app.route('/layout')
def layout():
    return render_template("layout.html")



if __name__ == '__main__':
    app.run(debug=True)
