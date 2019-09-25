# This is where our intial database configuration will be written
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

# create visualization info class
class Visual_Table(DB.Model):
    # __tablename__ = "all_urls"
    id = DB.Column(DB.Integer, primary_key=True)
    TIC_ID = DB.Column(DB.BigInteger, nullable=False)
    dataURL = DB.Column(DB.String(100))
    def __repr__(self):
        return '(TIC_ID %r, url %r)' %(self.tic_id, self.data_url)

# class 