from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from datetime import date
import json
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

studies_path = "static/files/studies.json"
projects_path = "static/files/projects.json"
works_path = "static/files/works.json"
skills_path = 'static/files/skills.json'
certificates_path = "static/assets/certificates"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/", methods=['GET'])
def home():
    return render_template('index.html', date=date.today().year)


@app.route("/education-work", methods=['GET'])
def education():
    with open(studies_path, 'r') as file:
        studies = json.load(file)
    with open(works_path, 'r') as file:
        works = json.load(file)
    return render_template('education.html',
                           studies=studies, works=works, date=date.today().year,
                           len_studies=len(studies), len_works=len(works))


@app.route("/projects", methods=['GET'])
def projects():
    with open(projects_path, 'r') as file:
        project = json.load(file)

    return render_template('projects.html', projects=project, len_projects=len(project),
                           date=date.today().year)


@app.route("/skills", methods=['GET'])
def skills():
    with open(skills_path, 'r') as file:
        skill = json.load(file)
    return render_template("skills.html", date=date.today().year, skills=skill)


@app.route("/certificates", methods=['GET'])
def certificates():
    my_certificates = []

    for root, directories, files in os.walk(certificates_path):
        for filename in files:
            my_certificates.append(filename)

    return render_template("certificates.html", date=date.today().year,
                           my_certificates=my_certificates, len_certificates=len(my_certificates))


@app.route("/about", methods=['GET'])
def about():
    return render_template("about.html", date=date.today().year)


@app.route("/get_in_touch", methods=['GET', 'POST'])
def get_in_touch():
    form = ContactForm()
    text = request.args.get('text')
    if not text:
        text = "I would like to get in touch with you!"
    if form.validate_on_submit():
        smtp_user = os.getenv('GMAIL_USER')
        smtp_password = os.getenv('GMAIL_PASSWORD')

        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        from_email = smtp_user
        to_email = smtp_user

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = f'Connect with you on business!'

        body = (f'I am {form.name.data}\nMy email: {form.email.data}\n'
                f'My number: {form.phone.data}\nMessage: {form.message.data}')
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")
        finally:
            server.quit()

        return redirect(url_for('get_in_touch', text="Message successfully sent!"))

    return render_template("touch.html", date=date.today().year, form=form,
                           text=text)


if __name__ == "__main__":
    app.run(debug=True)
