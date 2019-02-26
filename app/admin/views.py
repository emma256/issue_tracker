
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from app.admin.forms import DepartmentForm, EmployeeAssignForm, IssueForm
from ..models import Department, Employee, Issue
from .. import db



def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# Department Views


@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    check_admin()

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")


@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")


@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")


@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")

@admin.route('/issues')
@login_required
def list_issues():
    check_admin

    issues = Issue.query.all()
    return render_template('admin/issues/issues.html',
                           issues=issues, title='Issues')


@admin.route('/issues/add', methods=['GET', 'POST'])
def add_issue():
    
    add_issue = True

    form = IssueForm()
    if form.validate_on_submit():
        issue = Issue(name=form.name.data,
                    description=form.description.data)

        try:
            db.session.add(issue)
            db.session.commit()
            flash('You have successfully added an issue.')
        except:

            flash('Error: issue already exists.')

        return redirect(url_for('auth.list_issues'))

    
    return render_template('auth/issues/issue.html', add_issue=add_issue,
                           form=form, title='Add Issue')


@admin.route('/issue/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_issue(id):
    
    check_admin()

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
        return redirect(url_for('admin.list_issues'))

    form.description.data = issue.description
    form.name.data = issue.name
    return render_template('admin/issues/issue.html', add_issue=add_issue,
                           form=form, title="Edit issue")


@admin.route('/issues/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_issue(id):
    """
    Delete a issue from the database
    """
    check_admin()

    issue = Issue.query.get_or_404(id)
    db.session.delete(issue)
    db.session.commit()
    flash('You have successfully deleted the issue.')

    # redirect to the issues page
    return redirect(url_for('admin.list_issues'))

    return render_template(title="Delete Issue")



@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')