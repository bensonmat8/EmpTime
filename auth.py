from flask import Blueprint, render_template

auth_bp = Blueprint('auth_bp', __name__, static_folder='static',
                    template_folder='templates')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    pass


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    pass
