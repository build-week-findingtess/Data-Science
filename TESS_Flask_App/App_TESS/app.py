"""Main Application and routing Logic for TESS Flask App"""
from decouple import config
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from .models import DB
import pandas as pd


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
        
        # pull example data from Notebooks folder. Will be be pulled from sql DB in the future
        data = pd.read_csv('../../Notebooks/tic_catalog_example.csv')

        # test_css is the css settings for the table. first item in titles will be ignored because of loop in Home.html
        return render_template('home.html',tables=[data.to_html(classes='test_css')], titles = ['na','Star Stuff'])

    return app
    
    