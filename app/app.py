from flask import Flask, render_template

app = Flask(__name__)

@app.route('/',methods=['GET'])
def homepage(request=None):
    return render_template('index.html')

@app.route('/add-patients', methods=['POST','GET'])
def add_patients(request=None):
    
    if request.method == 'GET':
        return render_template('add_patients.html')
    
@app.route('/list-patients', methods=['GET'])
def list_patients(request=None):
    if request.method == 'GET':
        return render_template('list_patients.html')
    else:
        return render_template('bad_request.html')
    
@app.route('/delete-patient', methods=['DELETE','GET'])
def delete_patient(request=None):
    if request.method == 'DELETE':
        return render_template('add_patients.html')

if __name__ == "__main__":
    app.run()