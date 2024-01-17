from flask import Flask, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from form import UserInputForm
#from models import IncomeExpenses
from views import views

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/views")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expensesDB.db'
app.config['SECRET_KEY'] = 'cake1788'

db = SQLAlchemy(app)

#with app.app_context():
 #   db.create_all()

if __name__ == "__main__":
    app.run('127.0.0.1', debug=True)



