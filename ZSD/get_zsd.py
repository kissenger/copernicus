import os
import copernicusmarine 
from dotenv import load_dotenv

load_dotenv()

copernicusmarine.login(
  username = os.getenv("USRNM"),
  password = os.getenv("PASSWD")
)

copernicusmarine.describe()

copernicusmarine.subset(
  dataset_id='cmems_obs-oc_atl_bgc-transp_my_l3-multi-1km_P1D',
  variables=["ZSD"],
  minimum_longitude=-8,
  maximum_longitude=2,
  minimum_latitude=49,
  maximum_latitude=60,
  start_datetime="2010-01-01T00:00:00",
  end_datetime="2024-12-31T23:59:59",
  output_filename = "zsd_2010_2024.nc",
  output_directory = "."    
)