import os
import copernicusmarine 
from dotenv import load_dotenv

load_dotenv()

# Data source:
# https://data.marine.copernicus.eu/product/OCEANCOLOUR_ATL_BGC_L3_MY_009_113/services

copernicusmarine.login(
  username = os.getenv("USRNAME"),
  password = os.getenv("PASSWD")
)

copernicusmarine.describe()

copernicusmarine.subset(
  dataset_id='cmems_obs-oc_atl_bgc-plankton_my_l3-olci-300m_P1D',
  variables=["CHL"],
  minimum_longitude=-8,
  maximum_longitude=2,
  minimum_latitude=49,
  maximum_latitude=60,
  start_datetime="2017-01-01T00:00:00",
  end_datetime="2024-12-31T23:59:59",
  output_filename = "plank2017-2024.nc",
  output_directory = "copernicus-data"    
)