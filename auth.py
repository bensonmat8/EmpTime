from datetime import datetime
from flask import Blueprint, render_template, flash, request, session, url_for, redirect
from flask_login import login_required, logout_user, current_user, login_user
from forms import LoginForm, SignupForm
from models import AppTable, db, User, UserAppAccess

auth_bp = Blueprint('auth_bp', __name__, static_folder='static',
                    template_folder='templates')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('auth_bp.landing'))
    if form.validate_on_submit():
        user = User.query.get(form.empid.data)
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('auth_bp.landing'))
        flash('Invalid username/password')
    return render_template('login.html', form=form)


@auth_bp.route('/landing', methods=['GET'])
def landing():
    return '<h1>Landing Under Construction<h1>'


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User Sign-up page
    GET request serve sign-up page
    POST request validates form and creates user
    """
    form = SignupForm(request.form)
    one = [['Icecream', 'Chocolate', 'Coffee', 'Lemonade', 'Water'],
           ['Is', 'Has', 'Was', 'UsedToBe', '']]
    # print(form.validate_on_submit())
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
            # db.session.commit()
            app = AppTable.query.get(0)
            userApp = UserAppAccess(role='admin',
                                    created_on=datetime.now(), created_by='Admin')
            userApp.apps = app
            userApp.user_dtl = user
            # db.session.add(user)
            db.session.commit()
            flash(f"{form.name.data}'s account created")
        else:
            flash(f'User {form.name.data} already in the system')
    elif request.method != 'GET':
        #flash('Contact Admin')
        for err in form.errors:
            flash(form.errors[err][0])
    return render_template('signup.html', title='Create an Account', form=form)
