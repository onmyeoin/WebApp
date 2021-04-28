import os
from myproject import app,db
from flask import render_template, redirect, request, url_for, flash, abort, send_file
from flask_login import login_user,login_required,logout_user
from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm
from myproject.reporting import create_VAT_Report
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    if request.method == 'POST':
        sales_report = request.files['file']
        if sales_report.filename != '':
            filename = sales_report.filename
            xls_filename = filename[:-3]+"xls"
            sales_report.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            csv_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            xls_path = os.path.join(app.config['REPORTS_FOLDER'], xls_filename)
            create_VAT_Report(csv_path,xls_path)
            '''
            Delete from UPLOAD FOLDER
            Delete from REPORTS FOLDER
            '''
        return send_file(f'../reports/{xls_filename}',mimetype='xls',attachment_filename=f'{xls_filename}',as_attachment=True)
    return render_template('reports.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
    #return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
