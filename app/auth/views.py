from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user, UserMixin 

from . import auth
from app.auth.forms import LoginForm, RegistrationForm, IssueForm
from .. import db
from ..models import Employee, Issue


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        # add employee to the database
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

    
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(
                form.password.data):
            # log employee in
            login_user(employee)

            if employee.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))

@auth.route('/issues')
@login_required
def list_issues():

    issues = Issue.query.all()
    return render_template('auth/issues/issues.html',
                           issues=issues, title='Issues')


@auth.route('/issues/add', methods=['GET', 'POST'])

def add_issue():
    
    add_issue = True

    form = IssueForm()
    if form.validate_on_submit():
        issue = Issue(name=form.name.data,
                    description=form.description.data)

        try:
            # add issue to the database
            db.session.add(issue)
            db.session.commit()
            flash('You have successfully added an issue.')
        except:
            # in case issue name already exists
            flash('Error: issue already exists.')

        # redirect to the issues page
        return redirect(url_for('auth.list_issues'))

    # load issue template
    return render_template('auth/issues/issue.html', add_issue=add_issue,
                           form=form, title='Add Issue')


@auth.route('/issue/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_issue(id):
    

    add_issue = False

    issue = Issue.query.get_or_404(id)
    form = IssueForm(obj=issue)
    if form.validate_on_submit():
        issue.name = form.name.data
        issue.description = form.description.data
        db.session.add(issue)
        db.session.commit()
        flash('You have successfully edited the issue.')

        # redirect to the issues page
        return redirect(url_for('auth.list_issues'))

    form.description.data = issue.description
    form.name.data = issue.name
    return render_template('auth/issues/issue.html', add_issue=add_issue,
                           form=form, title="Edit issue")


@auth.route('/issues/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_issue(id):
    
    issue = Issue.query.get_or_404(id)
    db.session.delete(issue)
    db.session.commit()
    flash('You have successfully deleted the issue.')

    # redirect to the issues page
    return redirect(url_for('auth.list_issues'))

    return render_template(title="Delete Issue")