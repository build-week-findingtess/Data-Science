"""Main Application and routing Logic for TESS Flask App"""
from decouple import config
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from .models import *
from .light_curve import *
from .Data_in import *

def create_app():
    """create and config an instance of the Flask App"""
    app = Flask(__name__)

    # configure DB, will need to update this when changing DBs?
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ENV'] = config('ENV')
    DB.init_app(app)

    # Create home route
    @app.route('/')
    def root():

 	# Pull example data from Notebooks folder. Will be be pulled from sql DB in the future.
        data = pd.read_csv('../../Notebooks/tic_catalog_example.csv')
        data = data.drop(columns ='Unnamed: 0')

        # test_css is the css settings for the table. first item in titles will be ignored because of loop in Home.html
        return render_template('home.html',tables = data, titles = ['na','Star Dataset'])     
    return app

    
    @app.route('/total_reset')
    def total_reset():
        DB.drop_all()
        DB.create_all()
        get_visual_data()
        get_toi_data()
        get_tic_catalog()
        return render_template('home.html', title='Reset Database!')

    return app
    