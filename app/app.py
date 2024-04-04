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
    def __repr__(self):
        return f"<Patient {self.name}>"

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
        patient_data = {}
        try:
            for element in names:
                patient_data[element] = request.form.get(element)
        except:
            abort(405, description="Something went wrong while getting patient data")
        patient = Patient(
            PESEL=int(patient_data["PESEL"]),
            name=patient_data["name"],
            surname=patient_data["surname"],
            street=patient_data["street"],
            city=patient_data["city"],
            zip_code=patient_data["zip_code"],
        )
        db.session.add(patient)
        db.session.commit()
        return render_template("add_patients.html",message="Patient added successfully")
    elif request.method == "GET":
        return render_template("add_patients.html")

@app.route("/list-patients", methods=["GET"])
def list_patients():
    if request.method == "GET":
        names=[]
        patients=[]
        message = "Here all of the search or sorted patients will be listed"
        return render_template("list_patients.html",atients=patients,names=names,message=message)


@app.route("/list-patients-search", methods=["POST"])
def list_patients_search():

    def search_patient(x):
        patient,option,value = x
        if re.search(value,patient[option]):
            return True
        else:
            return False

    if request.method == "POST":
        value=request.form["search"]
        option=request.form["option"]
        sort_by = request.form["sort-by"]
        
        # Here I am not sure how to get an attribute of an database object that is given in string
        # So I rewrite all of the data into a dictionary, it might not be the best way to do it
        message = "The list of patients is empty"
        patients_list=Patient.query.all()
        patients = [ { "PESEL":patient.PESEL, "name":patient.name, "surname":patient.surname, "street":patient.street, "city":patient.city, "zip_code":patient.zip_code } for patient in patients_list ] 
        names=["PESEL", "name", "surname", "street", "city", "zip_code"]
        patients_to_search = [ (patient,option,value) for patient in patients ]
        patients_to_search = filter(search_patient,patients_to_search)
        patients = [ patient for patient, option, value in patients_to_search ]
        if sort_by != "none":
            patients = sorted(patients,key=lambda patient: patient[sort_by])
        if len(patients) != 0:
            if sort_by != "none":
                message = f"List of all patients for query \"{value}\" sorted by {sort_by}"
            else:
                message = f"List of all patients for query \"{value}\" sorted by PESEL"
        return render_template("list_patients.html",patients=patients,names=names, message=message)
    else:
        abort(405,description="Method not allowed")
@app.route("/list-patients-sort", methods=["POST"])
def list_patients_sort():
    if request.method == "POST":
        message = "The list of patients is empty"
        option = request.form["option"]
        patients_list=Patient.query.all()
        patients = [ { "PESEL":patient.PESEL, "name":patient.name, "surname":patient.surname, "street":patient.street, "city":patient.city, "zip_code":patient.zip_code } for patient in patients_list ] 
        names=["PESEL", "name", "surname", "street", "city", "zip_code"]
        patients = sorted(patients,key=lambda patient: patient[option])
        if len(patients) != 0:
            message = f"List of patients sorted by {option}"
        return render_template("list_patients.html",patients=patients,names=names,message=message)
    else:
        abort(405,description="Method not allowed")

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
                abort(500, description=str(e))
            return render_template('delete_patient.html',message="Patient deleted successfully")
        else:
            return render_template('delete_patient.html',message="Patient doesn't exist in the database")
    elif request.method == "GET":
        return render_template("delete_patient.html")
    else:
        abort(405, description="Bad request")

@app.route("/edit-patient", methods=["GET","POST"])
def edit_patient():
    if request.method == "GET":
        return render_template("edit_patient.html")
    
    elif request.method == "POST":
        try:
            option = request.form["option"]
            PESEL = request.form["PESEL"]
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
        abort(405, description="Method not allowed")


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
