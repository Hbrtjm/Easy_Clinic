from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
import os.path

db = SQLAlchemy()
app = Flask(__name__)
db_name = 'Patients.db'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, db_name)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# initialize the app with Flask-SQLAlchemy
db.init_app(app)
class Patient(db.Model):
    PESEL = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    surname = db.Column(db.String(200))
    # date_of_creation = db.Column(db.Datetime(), default=datetime)
    street = db.Column(db.String(200))
    city = db.Column(db.String(200))
    zip_code = db.Column(db.String(7))


# db.create_all()


@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")


@app.route("/add-patients", methods=["POST", "GET"])
def add_patients():
    names = ["PESEL", "name", "surname", "street", "city", "zip_code"]
    dictionary = {}
    try:
        for element in names:
            dictionary[element] = request.form.get(element)
    except:
        return render_template("bad_request.html")
    if request.method == "POST":
        patient = Patient(
            PESEL=dictionary["PESEL"],
            name=dictionary["name"],
            surname=dictionary["surname"],
            street=dictionary["street"],
            city=dictionary["city"],
            zip_code=dictionary["zip_code"],
        )
        db.session.add(patient)
        db.session.commit()
    elif request.method == "GET":
        return render_template("add_patients.html")


@app.route("/list-patients", methods=["GET"])
def list_patients():
    if request.method == "GET":
        try:    
            search = f'.*{request.form.get("search")}.*'
            db.session.get()
        except:
            return render_template("list_patients.html")


@app.route("/delete-patients", methods=["DELETE", "GET"])
def delete_patient():
    if request.method == "DELETE":
        return render_template("delete_patients.html")
    elif request.method == "GET":
        pass
    else:
        return render_template("bad_request.html")


@app.route("/edit-patient", methods=["EDIT", "GET"])
def edit_patient():
    if request.method == "EDIT":
        return render_template("edit_patient.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("not_found.html")


if __name__ == "__main__":
    # app.create_all()
    app.run()
