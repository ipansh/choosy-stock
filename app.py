from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, TextAreaField, SubmitField
import os
import psycopg2

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] =  #os.getenv('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'mysecretkey'

db = SQLAlchemy(app)

class InfoForm(FlaskForm):
    '''
    This general class gets all forms submitted on the main page.
    '''
    invest_amount = StringField('How much are you willing to invest?')
    pref_industry = SelectField('Which industries would you like to focus on?', choices=[('pescetarian','pescetarian'),('omnivore','omnivore'),('vegetarian','vegetarian'),('vegan','vegan')])
    pref_growth = SelectField('What growth expectations do you have?')
    pref_risk = SelectField('What level of risk can you tolerate?')
    submit = SubmitField('Submit')

# Create our database model
class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(120), unique=True)
    company_name = db.Column(db.String(255), unique=False)
    industry = db.Column(db.String(255), unique=False)
    last_close_price = db.Column(db.Float, unique=False)
    yoy_growth = db.Column(db.Float, unique=False)
    volatility = db.Column(db.Float, unique=False)
    la_ratio = db.Column(db.Float, unique=False)
    net_profit_margin = db.Column(db.Float, unique=False)
    pe_ratio = db.Column(db.Float, unique=False)

    def __init__(self, id, ticker, company_name, industry, last_close_price, yoy_growth, volatility, la_ratio, net_profit_margin, pe_ratio):
        self.id = id
        self.ticker = ticker
        self.diet = industry
        self.last_close_price = last_close_price
        self.yoy_growth = yoy_growth
        self.volatility = volatility
        self.la_ratio = la_ratio
        self.net_profit_margin = net_profit_margin
        self.pe_ratio = pe_ratio

    def __repr__(self):
        return '<Company Ticker %r>' % self.ticker

@app.route("/",  methods = ['GET','POST'])
def home():

    db.create_all()

    form = InfoForm()

    if form.validate_on_submit():
        invest_amount = form.invest_amount.data
        pref_industry = form.pref_industry.data
        pref_growth = form.pref_growth.data
        pref_risk = form.pref_risk.data
        submit = form.submit.data

        print(invest_amount, pref_industry, pref_growth, pref_risk, submit)

        return redirect(url_for('portfolio'))

    return render_template('home.html')

@app.route("/portfolio")
def portfolio():
    return render_template('portfolio.html')
    

if __name__  == '__main__': 
    app.run(debug=True)