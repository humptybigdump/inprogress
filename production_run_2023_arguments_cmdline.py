import sys
import gcsfs
import jax
import numpy as np
import pickle
import xarray
from datetime import datetime, timedelta
from dinosaur import horizontal_interpolation, spherical_harmonic, xarray_utils
import neuralgcm

# Ensure recursion limit is adequate
sys.setrecursionlimit(100000)

# Check for required arguments
if len(sys.argv) != 3:
    print("Usage: python script_name.py <start_month> <end_month>")
    sys.exit(1)

# Parse start and end months from command line arguments
try:
    start_month = int(sys.argv[1])
    end_month = int(sys.argv[2])
except ValueError:
    print("Error: start_month and end_month must be integers.")
    sys.exit(1)

# Validate month ranges
if not (1 <= start_month <= 12) or not (1 <= end_month <= 12):
    print("Error: Months must be between 1 and 12.")
    sys.exit(1)

# Set up GCS and model
gcs = gcsfs.GCSFileSystem(token='anon')

model_name = 'neuralgcm_04_30_2024_neural_gcm_dynamic_forcing_deterministic_2_8_deg.pkl'
local_path = '/root/workspace/ai-models-forecast/neuralgcm/pretrained_models/' + model_name

# Open the pickle file and load the checkpoint
with open(local_path, 'rb') as f:
    ckpt = pickle.load(f)

model = neuralgcm.PressureLevelModel.from_checkpoint(ckpt)

era5_path = 'gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3'
full_era5 = xarray.open_zarr(gcs.get_mapper(era5_path), chunks=None)

# Configure date range using the start and end months provided
start_date = datetime(2023, start_month, 1)
end_date = datetime(2023, end_month, 1)

# Adjust end_date to the last day of the end_month
end_date = (end_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)

print(f"Configured date range: {start_date} to {end_date}")

# The rest of your script would follow here

# ERA5 regridding setup                                                                                                                                                                                            
era5_grid = spherical_harmonic.Grid(
    latitude_nodes=full_era5.sizes['latitude'],
    longitude_nodes=full_era5.sizes['longitude'],
    latitude_spacing=xarray_utils.infer_latitude_spacing(full_era5.latitude),
    longitude_offset=xarray_utils.infer_longitude_offset(full_era5.longitude),
)
regridder = horizontal_interpolation.ConservativeRegridder(
    era5_grid, model.data_coords.horizontal, skipna=True
)

# Time processing loop                                                                                                                                                                                             
current_date = start_date
while current_date <= end_date:
    demo_start_time = current_date.strftime('%Y-%m-%d')
    demo_end_time = (current_date + timedelta(days=1)).strftime('%Y-%m-%d')

    # Select and preprocess ERA5 data for the day                                                                                                                                                                  
    sliced_era5 = (
        full_era5
        [model.input_variables + model.forcing_variables]
        .pipe(
            xarray_utils.selective_temporal_shift,
            variables=model.forcing_variables,
            time_shift='24 hours',
        )
        .sel(time=slice(demo_start_time, demo_end_time))
        .compute()
    )
    eval_era5 = xarray_utils.regrid(sliced_era5, regridder)
    eval_era5 = xarray_utils.fill_nan_with_nearest(eval_era5)


    # Model setup for the day                                                                                                                                                                              
    inner_steps = 24  # save model outputs once every 24 hours                                                                                                                                             
    outer_steps = 15 * 24 // inner_steps  # total of 15 days                                                                                                                                               
    timedelta_np = np.timedelta64(1, 'h') * inner_steps
    times = np.arange(outer_steps) * inner_steps  # time axis in hours       
    # Initialize model state
    inputs = model.inputs_from_xarray(eval_era5.isel(time=0))
    input_forcings = model.forcings_from_xarray(eval_era5.isel(time=0))
    rng_key = jax.random.key(42)  # optional for deterministic models                                                                                                                                              
    initial_state = model.encode(inputs, input_forcings, rng_key)

    # Use persistence for forcing variables (SST and sea ice cover)                                                                                                                                                
    all_forcings = model.forcings_from_xarray(eval_era5.head(time=1))

    # Run forecast                                                                                                                                                                                                 
    final_state, predictions = model.unroll(
        initial_state,
        all_forcings,
        steps=outer_steps,
        timedelta=timedelta_np,
        start_with_input=True,
    )
    predictions_ds = model.data_to_xarray(predictions, times=times)

    # Save output to NetCDF                                                                                                                                                                                        
    output_file = f'/root/workspace/ai-models-forecast/neuralgcm/ERA5_2023/{demo_start_time}_forecast.nc'
    predictions_ds.to_netcdf(output_file)

    print(f"Processed and saved predictions for {demo_start_time}")

    # Move to the next day                                                                                                                                                                                         
    current_date += timedelta(days=1)
