#from app import app
from flask import Flask, Blueprint, render_template, request, jsonify, flash, redirect, url_for, get_flashed_messages
from form import UserInputForm
import json

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html") 

@views.route("/portfolio")
def portfolio():
    return render_template("Portfolio.html")

@views.route("/dashboards")
def dashboards():
    from app import db, app
    from models import IncomeExpenses
    with app.app_context():
        entries = IncomeExpenses.query.order_by(IncomeExpenses.date.desc()).all()
    return render_template("dashboards.html", entries = entries)


@views.route("/add", methods = ["GET", "POST"])
def add_expense():
    from models import IncomeExpenses
    from app import db, app
    form = UserInputForm()
    if form.validate_on_submit():
        entry = IncomeExpenses(type=form.type.data, amount=form.amount.data, 
                               category = form.category.data)
        with app.app_context():
            db.session.add(entry)
            db.session.commit()
        flash("Successful entry", 'success')
        return redirect(url_for('views.add_expense'))
    return render_template("add.html", title = 'add', form = form)

@views.route('/delete-post/<int:entry_id>')
def delete(entry_id):
    from models import IncomeExpenses
    from app import db, app
    with app.app_context():
        entry = IncomeExpenses.query.get_or_404(int(entry_id))
        db.session.delete(entry)
        db.session.commit()
    flash("Entry deleted", "success")
    return redirect(url_for("views.dashboards"))

@views.route('/chart')
def chart():
    from models import IncomeExpenses
    from app import db, app

    with app.app_context():
        income_vs_expense = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.type).group_by(IncomeExpenses.type).order_by(IncomeExpenses.type).all()
        category_comparison = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.category).group_by(IncomeExpenses.category).order_by(IncomeExpenses.category).all()
        dates = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.date).group_by(IncomeExpenses.date).order_by(IncomeExpenses.date).all()

    income_category = []
    for amounts, _ in category_comparison:
        income_category.append(amounts)

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)

    over_time_expenditure = []
    dates_label = []
    for amount, date in dates:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_expenditure.append(amount)

    return render_template('chart.html',
                            income_vs_expense=json.dumps(income_expense),
                            income_category=json.dumps(income_category),
                            over_time_expenditure=json.dumps(over_time_expenditure),
                            dates_label =json.dumps(dates_label)
                        )