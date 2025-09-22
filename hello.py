from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Email, ValidationError

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'eec7efe2-f705-4f2b-8baf-e2f92e3b3578'

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField('What is your UofT Email Address?', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')


@app.route('/user/<name>')
def user(name):
    current_time = datetime.utcnow()  # naive UTC datetime

    #current_time = now.astimezone()
    print("Current time passed:", current_time)
    return render_template('user.html', name=name, current_time = current_time)



@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_email is not None and old_email!= form.email.data:
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        session['email'] = form.email.data

        if ("utoronto" not in form.email.data):
            session['email'] = None
        return redirect(url_for('index'))
    
    return render_template('index.html',
        form = form, name = session.get('name'),  email = session.get('email'))

if __name__ == '__main__':
    app.run(debug=True)
