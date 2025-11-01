import os
import copernicusmarine 
from dotenv import load_dotenv

load_dotenv()

# Data source:
# https://data.marine.copernicus.eu/product/OCEANCOLOUR_GLO_BGC_L4_MY_009_104/description

copernicusmarine.login(
  username = os.getenv("USRNAME"),
  password = os.getenv("PASSWD")
)

copernicusmarine.describe()

copernicusmarine.subset(
  dataset_id='cmems_obs-oc_atl_bgc-transp_my_l3-multi-1km_P1D',
  variables=["SPM"],
  minimum_longitude=-8,
  maximum_longitude=2,
  minimum_latitude=49,
  maximum_latitude=60,
  start_datetime="2010-01-01T00:00:00",
  end_datetime="2024-12-31T23:59:59",
  output_filename = "spm_raw_data.nc",
  output_directory = "."    
)