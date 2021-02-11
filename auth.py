from flask import Blueprint, render_template
from forms import SignupForm

auth_bp = Blueprint('auth_bp', __name__, static_folder='static',
                    template_folder='templates')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return 'Under Construction'


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        pass
    return render_template('signup.html', title='Create an Account', form=form)
