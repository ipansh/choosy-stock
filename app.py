import os
#os.environ['DATABASE_URL'] = 'postgresql://hezuwrpkvlsmnb:dcf155aab6a3dc77ab94892f030c44e264611d3c01b4133e70d5839167bef9ee@ec2-3-224-157-224.compute-1.amazonaws.com:5432/db233hod6s79so'
#os.getenv('DATABASE_URL')

from flask import Flask, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = ''
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'mysecretkey'

db = SQLAlchemy(app)

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

@app.route("/")
def home():

    db.create_all()

    return render_template('home.html')

##more about forms here: https://overiq.com/flask-101/form-handling-in-flask/
@app.route("/portfolio", methods = ['POST'])
def portfolio():

    invest_amount_response = request.form.get("invest_amount")
    invest_industries_response = request.form.get("invest_industries")
    invest_risk_response = request.form.get("invest_risk")

    print(db.session.query(Company).filter(Company.industry in ['Information Technology']))

    return render_template('portfolio.html')

if __name__  == '__main__': 
    app.run(debug=True)
