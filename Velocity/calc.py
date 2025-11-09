import xarray as xr
import numpy as np
import os 

# Define your file paths clearly
INPUT_FILE = './vel_hrly_2024.nc'
OUTPUT_FILE = './vel_max.nc'

def calculate_and_save_max_velocity_magnitude(input_file_path, output_file_path):
    """
    Imports uo and vo velocity components from an input NetCDF file, 
    calculates the maximum velocity magnitude across the time dimension, 
    and saves the result to a specified output NetCDF file.

    Args:
        input_file_path (str): The path to the input NetCDF file (containing uo, vo).
        output_file_path (str): The path where the resulting max velocity NetCDF 
                                file should be saved.
    """
    print(f"🔄 Starting calculation for file: {input_file_path}")
    
    try:
        # 1. Open the NetCDF file using xarray (Lazy load)
        ds = xr.open_dataset(input_file_path)

        # 2. Extract the velocity components
        # Assuming variable names are 'uo' and 'vo'
        uo = ds['uo']
        vo = ds['vo']

        # 3. Calculate the velocity magnitude V = sqrt(uo^2 + vo^2)
        velocity_magnitude = np.sqrt(uo**2 + vo**2)

        # 4. Find the maximum velocity magnitude across the time dimension
        # This collapses the 'time' dimension, giving the annual maximum for each point
        max_velocity_magnitude = velocity_magnitude.max(dim='time')

        # 5. Save the result to the specified output NetCDF file
        max_velocity_magnitude.to_netcdf(output_file_path)

        print(max_velocity_magnitude)

        print(f"✅ Success! Maximum velocity magnitude saved to:")
        print(f"   -> {output_file_path}")

    except FileNotFoundError:
        print(f"❌ Error: File not found at {input_file_path}")
    except KeyError as e:
        print(f"❌ Error: Variable {e} not found in the input NetCDF file. Check variable names ('uo', 'vo').")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

# --- Usage Example ---



# Run the function with the defined arguments
calculate_and_save_max_velocity_magnitude(INPUT_FILE, OUTPUT_FILE)