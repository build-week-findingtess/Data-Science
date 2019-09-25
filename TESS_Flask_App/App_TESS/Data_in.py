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
def get_visual_data():
    # Start by emptying the table (maybe make this more elegant later?)
    # Visual_Table.query.delete()
    # conn = sqlite.connect(db.sqlite3)
    # cur = conn.cursor()  
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

    return dataproducts.to_sql(name='Visual_Table', con=DB.engine, index=False, 
                               if_exists='replace')


def get_toi_data():
    try: 
        # Getting labelled TESS Objects of Interest dataframe from Caltech:
        toi = pd.read_csv('https://exofop.ipac.caltech.edu/tess/' + 
                    'download_toi.php?sort=toi&output=csv')
    except:
        print('failed to import initial csv from caltech')
    else: 
        try:
            # Isolating columns we want:
            toi = toi[['TIC ID',
                'TOI',
                'Epoch (BJD)',
                'Period (days)',
                'Duration (hours)',
                'Depth (mmag)',
                'Planet Radius (R_Earth)',
                'Planet Insolation (Earth Flux)',
                'Planet Equil Temp (K)',
                'Planet SNR',
                'Stellar Distance (pc)',
                'Stellar log(g) (cm/s^2)',
                'Stellar Radius (R_Sun)',
                'TFOPWG Disposition',
                ]]
        except:
            print('failed to filter df')

    return toi.to_sql(name='TOI_Table', con=DB.engine, index=False, 
                               if_exists='replace')

def get_tic_catalog():
    # Getting additional data on TESS Objects of Interest from STScI:
    tic_catalog = pd.DataFrame()
    for tic_id in tqdm(toi['TIC ID'].unique()):
        row_data = Catalogs.query_criteria(catalog="Tic", ID=tic_id)
        row_data = row_data.to_pandas()
        tic_catalog = tic_catalog.append(row_data)
    tic_catalog = tic_catalog.reset_index(drop=True)

    # Renaming ID column to make this consistent with Caltech TOI dataframe:
    tic_catalog = tic_catalog.rename(columns={'ID': 'TIC ID'})

    # Isolating columns we want:
    tic_catalog = tic_catalog[['TIC ID',
                            'ra',
                            'dec',
                            'pmRA',
                            'pmDEC',
                            'plx',
                            'gallong',
                            'gallat',
                            'eclong',
                            'eclat',
                            'Tmag',
                            'Teff',
                            'logg',
                            'MH',
                            'rad',
                            'mass',
                            'rho',
                            'lum',
                            'd',
                            'ebv',
                            'numcont',
                            'contratio',
                            'priority']]

    return toi.to_sql(name='TIC_Cat_Table', con=DB.engine, index=False, 
                               if_exists='replace')
