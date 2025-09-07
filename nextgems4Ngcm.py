#=========================================================================================================================================
#==============================rename NextGEMS to feed to NueralGCM  =====================================================================
#=========================================================================================================================================
def var_rename_nextgems(ds):
    var_map = {
        'u': 'u_component_of_wind',
        'v': 'v_component_of_wind',
        't': 'temperature',
        'q': 'specific_humidity',
        'z': 'geopotential',  
        'land_sea_mask': 'land_sea_mask',  
        'ciwc': 'specific_cloud_ice_water_content',  
        'clwc': 'specific_cloud_liquid_water_content',  
        'ci': 'sea_ice_cover',  
        'sst': 'sea_surface_temperature',  
        'lat': 'latitude',
        'lon': 'longitude'
        }

    return ds.rename(var_map)

#=========================================================================================================================================
#================================== an ordinary linear interpolation using xarray!!!================================================
#=========================================================================================================================================
def vinterpolation_2_era37(ds):
    import gcsfs
    import xarray
    import numpy as np
    #==Reading ref ERA5 as reference
    gcs = gcsfs.GCSFileSystem(token='anon')
    era5_path = 'gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3'
    full_era5 = xarray.open_zarr(gcs.get_mapper(era5_path), chunks=None)
    ds37 = full_era5.level.values
    #== Existing vvertical levels
    ds25 = ds.level.values
    print("era5",ds37)
    print("nextgems",ds25)
    vars_3d = [var for var in ds.data_vars if 'level' in ds[var].dims]
    # print(vars_3d)
    interpolated_vars = {}
    del full_era5
    
    #== Interpolation#####################
    for var in vars_3d:
        print(var)
        interpolated_vars[var] = ds[var].interp(level=ds37) # linear
        
    ######################################
    #==Create a new dataset with interpolated 3D vars
    ds25_interp = xarray.Dataset(interpolated_vars)
    
    #==Add back non-interpolated variables if you want them included too
    for var in ds.data_vars:
        if var not in vars_3d:
            ds25_interp[var] = ds[var]    
    
    return ds25_interp
