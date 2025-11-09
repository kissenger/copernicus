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
  dataset_id='cmems_mod_glo_phy_my_0.083deg_static',
  variables=["deptho"],
  minimum_longitude=-8,
  maximum_longitude=2,
  minimum_latitude=49,
  maximum_latitude=60,
  output_filename = "depth_data.nc",
  output_directory = "."    
)