from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
import os.path
import glob


app = Flask(__name__)
app.secret_key = "jBIja3uLPrymArN452fMKdPnFJhgY1UYREoU5qad51b4aE0QgI4Dn6iGCmh8A8tQ"
db_name = 'Patients.db'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, db_name)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Patient(db.Model):
    PESEL = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    surname = db.Column(db.String(200))
    street = db.Column(db.String(200))
    city = db.Column(db.String(200))
    zip_code = db.Column(db.String(7))

@app.before_request
def create_database():
    if not glob.glob(BASE_DIR + '/Patients.db'):
        db.create_all()

@app.route("/", methods=["GET"])
def homepage():
    return render_template("homepage.html")


@app.route("/add-patients", methods=["POST", "GET"])
def add_patients():
    if request.method == "POST":
        names = ["PESEL", "name", "surname", "street", "city", "zip_code"]
        dictionary = {}
        print(request.form)
        try:
            for element in names:
                dictionary[element] = request.form.get(element)
            for element in names:
                print(dictionary[element])
        except:
            return render_template("bad_request.html")
        
        print(dictionary["name"])
        patient = Patient(
            PESEL=int(dictionary["PESEL"]),
            name=dictionary["name"],
            surname=dictionary["surname"],
            street=dictionary["street"],
            city=dictionary["city"],
            zip_code=dictionary["zip_code"],
        )
        db.session.add(patient)
        db.session.commit()
        return render_template("add_patients.html")
    elif request.method == "GET":
        return render_template("add_patients.html")

@app.route("/list-patients", methods=["GET"])
def list_patients():
    if request.method == "GET":
        names=[]
        patients=[]
        return render_template("list_patients.html",atients=patients,names=names)


@app.route("/list-patients-search", methods=["POST"])
def list_patients_search(option):
    value=request.form["searched_value"]
    patients_list=Patient.query.get()
    names=["PESEL", "name", "surname", "street", "city", "zip_code"]
    patients = [ { "PESEL":patient.PESEL, "name":patient.name, "surname":patient.surname, "street":patient.street, "city":patient.city, "zip_code":patient.zip_code } for patient in patients_list ] 
    if request.method == "POST":
        return render_template("list_patients.html",patients=patients,names=names)

@app.route("/list-patients-sort", methods=["POST"])
def list_patients_sort():
    option = request.form["option"]
    patients_list=Patient.query.all()
    patients = [ { "PESEL":patient.PESEL, "name":patient.name, "surname":patient.surname, "street":patient.street, "city":patient.city, "zip_code":patient.zip_code } for patient in patients_list ] 
    print(option)
    names=["PESEL", "name", "surname", "street", "city", "zip_code"]
    sorted(patients,key=lambda patient: patient[option])
    print(patients)
    if request.method == "POST":
        return render_template("list_patients.html",patients=patients,names=names)


@app.route("/delete-patient", methods=["POST", "GET"])
def delete_patient():
    if request.method == "POST":
        PESEL = request.form["PESEL"]    
        patient_to_delete = Patient.query.get(PESEL)
        if patient_to_delete:
            try:
                db.session.delete(patient_to_delete)
                db.session.commit()
            except Exception as e:
                flash(f'Error deleting patient: {e}', 'error')
            return render_template('delete_patient.html',message="Patient deleted successfully")
        else:
            return render_template('delete_patient.html',message="Patient doesn't exist in the database")
    elif request.method == "GET":
        return render_template("delete_patient.html")
    else:
        abort(400, description="Bad request")

@app.route("/edit-patients", methods=["GET","POST"])
def edit_patient():
    if request.method == "GET":
        return render_template("edit_patient.html")
    
    elif request.method == "POST":
        try:
            option = request.form["option"]
            PESEL = request.form["PESEL"]
            if not re("[0-9]{9}",PESEL):
                abort(400, description="PESEL is in the wrong format")
        except:
            abort(400, description="PESEL was not provided")
        patient_to_edit = Patient.query.get_or_404(PESEL)
        if not patient_to_edit:
            abort(404, description="Patient not found")

        data = request.form.get("modified_value") 
        if not data:
            abort(400, description="No data provided")
        if hasattr(patient_to_edit, option):
            setattr(patient_to_edit, option, data)
        else:
            abort(400, description=f"Invalid field: {option}")

        try:
            db.session.commit()
            return render_template("edit_patient.html",message="Patient updated successfully!")
        except Exception as e:
            abort(500, description=str(e))
    else:
        abort(400, description="Wrong http method")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("not_found.html")

@app.errorhandler(400)
def bad_request(e):
    return render_template("bad_request.html")

@app.errorhandler(500)
def bad_request(e):
    return render_template("internal_server_error.html")

@app.errorhandler(405)
def bad_request(e):
    return render_template("method_not_allowed.html")

if __name__ == "__main__":
    app.run()
