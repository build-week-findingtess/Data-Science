import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from astropy.io import fits
import matplotlib.pyplot as plt
from .models import DB, Visual_Table

# fetch Light Curve visual and basic data
def get_lightcurve(input_tic):
    # Getting urls for all dataproducts associated with TIC ID given by user
    try:

        # Next line need to become a DB query 
        # urls_for_input = dataproducts[dataproducts['TIC ID'] == input_tic][
        # 'dataURL'].tolist()
        urls_for_input = DB.query.filter(Visual_Table.TIC_ID == input_tic).tolist()


        for url in urls_for_input:
        
            fits_file = ('https://mast.stsci.edu/api/v0.1/Download/file?uri=' + url)
        
            print(fits.info(fits_file), "\n")
            print(fits.getdata(fits_file, ext=1).columns)
        
            with fits.open(fits_file, mode="readonly") as hdulist:
                tess_bjds = hdulist[1].data['TIME']
                sap_fluxes = hdulist[1].data['SAP_FLUX']
                pdcsap_fluxes = hdulist[1].data['PDCSAP_FLUX']
        
            fig, ax = plt.subplots()

            ax.plot(tess_bjds, pdcsap_fluxes, 'ko')

            ax.set_ylabel("PDCSAP Flux (e-/s)")
            ax.set_xlabel("Time (TBJD)")

            plt.show()
    except:
        print('Error ')
    return