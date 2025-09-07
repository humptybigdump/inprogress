import time
import jax
import numpy as np
import pickle
import xarray
from dinosaur import horizontal_interpolation
from dinosaur import spherical_harmonic
from dinosaur import xarray_utils
from datetime import datetime, timedelta
import jaxlib
import neuralgcm
import nextgems4Ngcm
import fsspec
import warnings
warnings.filterwarnings("ignore")

# Set up GCS and model                                                                                                                                                           
start = time.time()
model_sub_name = 'deterministic_2_8'
model_name = f'neural_gcm_dynamic_forcing_{model_sub_name}_deg.pkl'

with open(f'pretrained_models/neuralgcm_04_30_2024_{model_name}', 'rb') as f:
    ckpt = pickle.load(f)
model = neuralgcm.PressureLevelModel.from_checkpoint(ckpt)

# importing NextGEMS
nextgems_path = 'http://i42storage-node.kiklima.iti.kit.edu:9002/practical-ai-in-climate-and-environmental-science/next_gems'
ds = xarray.open_zarr(fsspec.get_mapper(nextgems_path),consolidated=True)

ds = nextgems4Ngcm.var_rename_nextgems(ds) # Change variable names for neuralgcm
next_gems = nextgems4Ngcm.vinterpolation_2_era37(ds) # interpolation from 25 vertical levels of original nextgems to 37 vertical levels needed for neuralGCM 
# print(ds)

# Configure date range for 2049                                                                                                                                
start_date = datetime(2049, 1, 24)
end_date = datetime(2049, 1, 25)

# ERA5 regridding setup                                                                                                                                                                                            
nextgems_grid = spherical_harmonic.Grid(
    latitude_nodes=next_gems.sizes['latitude'],
    longitude_nodes=next_gems.sizes['longitude'],
    latitude_spacing=xarray_utils.infer_latitude_spacing(next_gems.latitude),
    longitude_offset=xarray_utils.infer_longitude_offset(next_gems.longitude),
)
regridder = horizontal_interpolation.ConservativeRegridder(
    nextgems_grid, model.data_coords.horizontal, skipna=True
)

# Time processing loop                                                                                                                                        
print("Start forcasting...")
current_date = start_date
while current_date <= end_date:
    demo_start_time = current_date.strftime('%Y-%m-%d')
    demo_end_time = (current_date + timedelta(days=1)).strftime('%Y-%m-%d')

    # Select and preprocess ERA5 data for the day                                                                                                                                                                  
    sliced_nextgems = (
        next_gems
        [model.input_variables + model.forcing_variables]
        .pipe(
            xarray_utils.selective_temporal_shift,
            variables=model.forcing_variables,
            time_shift='24 hours',
        )
        .sel(time=slice(demo_start_time, demo_end_time))
        .compute()
    )
    eval_nextgems = xarray_utils.regrid(sliced_nextgems, regridder)
    eval_nextgems = xarray_utils.fill_nan_with_nearest(eval_nextgems)


    # Model setup for the day                                                                                                                                                                              
    inner_steps = 24  # save model outputs once every 24 hours                                                                                                                                             
    outer_steps = 3 * 24 // inner_steps  # total of 15 days                                                                                                                                               
    timedelta_np = np.timedelta64(1, 'h') * inner_steps
    times = np.arange(outer_steps) * inner_steps  # time axis in hours       
    # Initialize model state
    inputs = model.inputs_from_xarray(eval_nextgems.isel(time=0))
    input_forcings = model.forcings_from_xarray(eval_nextgems.isel(time=0))
    rng_key = jax.random.key(42)  # optional for deterministic models                                                                                                                                              
    initial_state = model.encode(inputs, input_forcings, rng_key)

    # Use persistence for forcing variables (SST and sea ice cover)                                                                                                                                                
    all_forcings = model.forcings_from_xarray(eval_nextgems.head(time=1))

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
    output_file = f'NEXTGEMS_2049/{demo_start_time}_forecast.nc'
    predictions_ds.to_netcdf(output_file)

    print(f"Processed and saved predictions for {demo_start_time}")

    # Move to the next day                                                                                                                                                                                         
    current_date += timedelta(days=1)
