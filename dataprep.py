import osfrom flask import Flask, render_template, requestfrom models import *app = Flask(__name__)app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Falsedb.init_app(app)def main():    dept = Department(dept_id=1, dept_name='Food and Nutrition')    db.session.add(dept)    db.session.commit()if __name__=='__main__':    with app.app_context():        main()