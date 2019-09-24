import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from astroquery.mast import Catalogs, Observations
from astropy.table import Table
from tqdm import tqdm
from .models import DB, Visual_Table
# from sqlalchemy import create_engine

# DB = SQLAlchemy()
# engine = create_engine('sqlite://', echo=False)

# Getting labelled TESS Objects of Interest dataframe from Caltech:


# fetch TIC IDs from caltech
def get_data():
    # Start by emptying the table (maybe make this more elegant later?)
    Visual_Table.query.delete()
    try:
        # Getting labelled TESS Objects of Interest dataframe from Caltech:
        toi = pd.read_csv('https://exofop.ipac.caltech.edu/tess/' + 
                  'download_toi.php?sort=toi&output=csv')
        # Isolating TIC IDs and TFOPWG Disposition values to use as target:
        toi = toi[['TIC ID', 'TFOPWG Disposition']]
        toi = toi.rename(columns={'TIC ID': 'TIC_ID'})

        # Getting additional data on TESS Objects of Interest from STScI:
        tic_catalog = pd.DataFrame()
        for tic_id in tqdm(toi['TIC_ID'].unique()):
            row_data = Catalogs.query_criteria(catalog="Tic", ID=tic_id)
            row_data = row_data.to_pandas()
            tic_catalog = tic_catalog.append(row_data)
        tic_catalog = tic_catalog.reset_index(drop=True)
        # Renaming ID column to make this consistent with Caltech TOI dataframe:
        tic_catalog = tic_catalog.rename(columns={'ID': 'TIC_ID'})

        # Getting all dataproducts for TESS Objects of Interest from STScI:
        dataproducts = pd.DataFrame()
        for tic_id in tqdm(toi['TIC_ID']):
            row_data = Observations.query_criteria(obs_collection="TESS",
                                                target_name=tic_id)
            row_data = row_data.to_pandas()
            dataproducts = dataproducts.append(row_data)
        dataproducts = dataproducts.reset_index(drop=True)
        # Isolating TIC IDs (target_name) and dataURL values to get associated files:
        dataproducts = dataproducts[['target_name', 'dataURL']]
        # Renaming ID column to make this consistent with Caltech TOI dataframe:
        dataproducts = dataproducts.rename(columns={'target_name': 'TIC_ID'})

    except Exception as e:
        print('Error importing data: ')
        raise e

    return dataproducts.to_sql(name='all_urls', con=DB.engine, if_exists='replace')
        # Move this df of tuples to sql. Also will need to move to postgress
         #, index=False)







        # Took this out of the get_data function...
        # useful_data = dataproducts[['target_name', 'target_name']]
        # # Not sure if the below will work...
        # for row in useful_data:
        #     pair = Visual_Table(tic_id = useful_data['target_name']
        #                         , data_url = useful_data['target_name'])
        #     DB.session.add(pair)

        # conn = sqlite.connect(db.sqlite3)
        # cur = conn.cursor()  
        # . . .
        # dataproducts.to_sql(name='all_urls', con=conn, index=False)
        # sqlite.commit()
        # cur.close()
        # conn.close()

# eventually we'll need to move towards postgress... EXAMPLE
# from sqlalchemy import create_engine
# engine = create_engine('postgresql://scott:tiger@localhost:5432/mydatabase')
# df.to_sql('table_name', engine)

# See: https://stackoverflow.com/questions/23103962/how-to-write-dataframe-to-postgres-table