import os
import copernicusmarine 
from dotenv import load_dotenv

load_dotenv()

# https://data.marine.copernicus.eu/product/SST_GLO_SST_L4_REP_OBSERVATIONS_010_024/services
# https://data.marine.copernicus.eu/product/SST_ATL_PHY_L3S_NRT_010_037/description?pk_vid=66414b225dc04fc51762024705020cb6
copernicusmarine.login(
  username = os.getenv("USRNAME"),
  password = os.getenv("PASSWD")
)

copernicusmarine.describe()

copernicusmarine.subset(
  dataset_id='cmems_mod_nws_phy-uv_my_7km-2D_PT1H-i',
  variables=["vo","uo"],
  minimum_longitude=-8,
  maximum_longitude=2,
  minimum_latitude=49,
  maximum_latitude=60,
  start_datetime="2024-01-01T00:00:00",
  end_datetime="2024-12-31T23:59:59",
  output_filename = "vel-hrly_2024.nc",
  output_directory = "."    
)