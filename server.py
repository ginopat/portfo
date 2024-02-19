from flask import Flask, render_template, url_for, request, redirect
import csv


app = Flask(__name__)

@app.route("/")
def my_home():
        return render_template('index.html')
    
@app.route("/<string:page_name>")
def my_route(page_name):
        return render_template(page_name)
    
def write_to_csv(data):
    with open('database.csv', newline = '', mode='a') as database:
        email= data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database, delimiter=',', quotechar= "'")
        csv_writer.writerow([email, subject, message])

@app.route("/submit_form", methods = ['POST','GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect('/thankyou.html')
    else:
        return "something went wrong, try again"
    