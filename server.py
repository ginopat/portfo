from flask import Flask, render_template, url_for, request, redirect
import csv
import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path


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

def send_email():
    html = Template(Path('email_contacts_template.html').read_text())
    email = EmailMessage()
    email['from'] = 'Gino Patricolo'
    email['to'] = 'gino.patricolo@gmail.com'
    email['subject'] = 'hai ricevuto una richiesta di contatto'
 
    email.set_content(html.substitute({'name': 'Gino'}), 'html')
    with open('database.csv', 'rb') as f:
        file_data = f.read()
    email.add_attachment(file_data, maintype='text', subtype='plain', filename='database.csv')
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
      smtp.ehlo()
      smtp.starttls()
      smtp.login('gino.patricolo@gmail.com', 'jwnidukforsecjay')
      smtp.send_message(email)
      print('all good boss!')

@app.route("/submit_form", methods = ['POST','GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        send_email()
        return redirect('/thankyou.html')
    else:
        return "something went wrong, try again"
