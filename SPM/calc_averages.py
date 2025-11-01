
import xarray as xr
import numpy as np

# --- Configuration ---
# 1. Define the input and output paths
INPUT_FILE = './spm_raw_data.nc'
OUTPUT_FILE = './spm_averages.nc'

# 2. Specify the name of the data variable you want to average
VARIABLE_NAME = 'SPM'
CHUNK_SIZE = 500  # Number of time steps to load for the annual calculation

# --- Script ---

def compute_qgis_compatible_final(input_file, output_file, var_name, chunk_size):
    """
    Computes 12 monthly climatologies and the annual mean/count, saving all 26 
    results as pure 2D variables (lat, lon) for maximum compatibility with GIS software.
    """
    print(f"Starting QGIS-compatible computation for variable: {var_name}")
    
    final_dataarrays = []
    output_encoding = {}

    # 1. Open the Dataset and load month index reliably
    try:
        ds = xr.open_dataset(input_file, decode_times=True)
        data_var = ds[var_name]
        # Pre-compute the month index once, upfront, reliably
        months_of_data = data_var['time.month'].load() 
    except Exception as e:
        print(f"\n❌ Error opening file or finding variable '{var_name}': {e}")
        return

    # Get spatial dimensions and coordinates once
    spatial_dims = data_var.dims[1:]
    spatial_coords = {dim: ds.coords[dim] for dim in spatial_dims}
    spatial_shape = data_var.shape[1:]
    time_dim_size = data_var.sizes['time']
    
    # --- 2. Calculate Monthly Climatologies (12 Layers - QGIS FIX APPLIED) ---
    print("\nCalculating 12 Monthly Climatologies (Saving as 2D Layers)...")
    
    for month in range(1, 13):
        label = f"month_{str(month).zfill(2)}"
        
        # Use explicit boolean indexing on the time coordinate
        month_mask = months_of_data == month
        
        # Select data using the mask (Lazy operation)
        data_subset = data_var.isel(time=month_mask)
        
        # Calculate the mean and count for the small subset (Compute step)
        monthly_mean_da = data_subset.mean(dim='time', skipna=True).compute()
        monthly_count_da = data_subset.count(dim='time').compute()
        
        # --- Create Final DataArrays (CRITICAL FIX: ONLY SPATIAL DIMS) ---
        
        # Mean DataArray (2D)
        mean_da = xr.DataArray(
            monthly_mean_da.values,
            coords=spatial_coords,                              # Only spatial coords
            dims=spatial_dims,                                  # Only spatial dims
            name=f'{var_name}_avg_{label}',
            attrs=data_var.attrs.copy()
        )
        final_dataarrays.append(mean_da)
        output_encoding[mean_da.name] = {'zlib': True, 'complevel': 4}

        # Count DataArray (2D)
        count_da = xr.DataArray(
            monthly_count_da.values, 
            coords=spatial_coords, 
            dims=spatial_dims, 
            name=f'{var_name}_count_{label}',
            attrs={'long_name': f'Number of valid observations for {label} average', 'units': '1'}
        )
        final_dataarrays.append(count_da)
        output_encoding[count_da.name] = {'zlib': True, 'complevel': 4, '_FillValue': -1, 'dtype': 'int32'}

        print(f"  ✅ Calculated and prepared 2D layer for Month {month}.")


    # --- 3. Calculate Overall Annual Mean and Count (Chunked Method - Unchanged) ---
    print("\nCalculating Overall Annual Average (Memory-Efficient Chunking)...")
    
    annual_sum = np.zeros(spatial_shape, dtype=np.float64) 
    annual_count = np.zeros(spatial_shape, dtype=np.int64) 
    
    # Iterate over time in chunks
    for i in range(0, time_dim_size, chunk_size):
        time_slice = slice(i, i + chunk_size)
        
        chunk = data_var.isel(time=time_slice).load()
        chunk_values = chunk.values
        
        for j in range(chunk_values.shape[0]):
            step_data = chunk_values[j]
            valid_mask = ~np.isnan(step_data)
            valid_coords = np.where(valid_mask)
            
            annual_sum[valid_coords] += step_data[valid_coords]
            annual_count[valid_coords] += 1
            
        print(f"  Processed time steps {i} to {min(i + chunk_size, time_dim_size)}")

    # Calculate final annual mean
    annual_mean = np.divide(
        annual_sum, annual_count, 
        out=np.full_like(annual_sum, np.nan, dtype=np.float64), 
        where=annual_count != 0
    )

    # --- Create Final Annual DataArrays (Already 2D) ---
    label = "overall_annual"
    layer_dims = spatial_dims
    
    # Mean DataArray
    mean_da = xr.DataArray(annual_mean, coords=spatial_coords, dims=layer_dims, 
                           name=f'{var_name}_avg_{label}', attrs=data_var.attrs.copy())
    final_dataarrays.append(mean_da)
    output_encoding[mean_da.name] = {'zlib': True, 'complevel': 4}

    # Count DataArray
    count_da = xr.DataArray(annual_count, coords=spatial_coords, dims=layer_dims, 
                           name=f'{var_name}_count_{label}',
                           attrs={'long_name': f'Number of valid observations for {label} average', 'units': '1'})
    final_dataarrays.append(count_da)
    output_encoding[count_da.name] = {'zlib': True, 'complevel': 4, '_FillValue': -1, 'dtype': 'int32'}
    
    print("  ✅ Calculated and prepared layer for Annual Average.")

    # 4. Combine and Save
    ds_out = xr.Dataset({da.name: da for da in final_dataarrays})

    print(f"\nSaving all 26 variables to {output_file}...")
    try:
        ds_out.to_netcdf(output_file, encoding=output_encoding)
        
        print(f"\n✅ Success! All 26 variables saved to: {output_file}")
        
    except Exception as e:
        print(f"  ❌ Error saving the combined file: {e}")

if __name__ == "__main__":
    compute_qgis_compatible_final(INPUT_FILE, OUTPUT_FILE, VARIABLE_NAME, CHUNK_SIZE)