from datetime import datetime
from flask import Blueprint, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from forms import SignupForm
from models import AppTable, db, User, UserAppAccess

auth_bp = Blueprint('auth_bp', __name__, static_folder='static',
                    template_folder='templates')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return 'Under Construction'


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User Sign-up page
    GET request serve sign-up page
    POST request validates form and creates user
    """
    app_exsist = AppTable.query.get(0)
    if app_exsist is None:
        app_exsist = AppTable(appid=0,
                              appName='Signup',
                              appRoute='PEI/signup')
        db.session.add(app_exsist)
        db.session.commit()
    form = SignupForm(request.form)
    one = [['Icecream', 'Chocolate', 'Coffee', 'Lemonade', 'Water'],
           ['Is', 'Has', 'Was', 'UsedToBe', '']]
    print(form.validate_on_submit())
    if form.validate_on_submit():
        existing_user = User.query.get(form.empid.data)
        if existing_user is None:
            user = User(empid=form.empid.data,
                        name=form.name.data,
                        email=form.email.data,
                        created_on=datetime.now(),
                        created_by='Admin',
                        last_login=datetime.now())
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            userApp = UserAppAccess(empid=form.empid.data, appid=0, role='admin',
                                    created_on=datetime.now(), created_by='Admin')
            db.session.add(userApp)
            db.session.commit()
            flash(f'User {form.name.data} created')
        else:
            flash(f'User {form.name.data} already in the system')
    elif request.method != 'GET':
        flash('Contact Admin')
        flash(form.errors)
    return render_template('signup.html', title='Create an Account', form=form)
