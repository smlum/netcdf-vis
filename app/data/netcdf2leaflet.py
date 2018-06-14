
# coding: utf-8

# In[2]:

from netCDF4 import Dataset, num2date
import numpy as np
import json


# In[4]:

# import data
dataset = Dataset('netcdf/echam_daily.nc')


# In[5]:

# interrogate dimensions
print(dataset.dimensions.keys())


# In[6]:

# interrogate variable structure
print(dataset.variables['u10'])


# In[13]:

# interrogate variables
# find the u and v wind data
print("Check variables:")
print(dataset.variables.keys())


# In[14]:

# USER input names for u and v wind variables
u_var = 'u10'
v_var = 'v10'
temp_var = 'tsurf'


# In[15]:

print("Check units:")
print(dataset.variables[u_var].units)
print(dataset.variables[temp_var].units)


# In[18]:

print("Check dimensions:")
print(dataset.variables[u_var].dimensions, dataset.variables[u_var].shape)
print(dataset.variables[u_var].dimensions, dataset.variables[temp_var].shape)


# In[19]:

# set header variables for wind
nx = dataset.variables[u_var].shape[1]
ny = dataset.variables[u_var].shape[2]
dx = 360 / nx
dy = 180 / ny
tot = nx * ny


# In[20]:

# get data for u wind
a = dataset.variables[u_var][:][0]
A = np.matrix(a)
b = A.flatten()
c = np.ravel(b).T
u_data = c.tolist()


# In[21]:

# get data for v wind
a = dataset.variables[v_var][:][0]
A = np.matrix(a)
b = A.flatten()
c = np.ravel(b).T
v_data = c.tolist()


# In[24]:

# format JSON
wind_data = [{
  "header": {
    "parameterNumberName": "eastward_wind",
    "parameterUnit": "m.s-1",
    "parameterNumber": 2,
    "parameterCategory": 2,
    "nx": nx,
    "ny": ny,
    "numberPoints": tot,
    "dx": dx,
    "dy": dy,
    "la1": 90.0,
    "lo1": 0.0,
    "la2": -90.0,
    "lo2": 360.0,
    "refTime": "2017-02-01 23:00:00"
  },
  "data": u_data
}, {
  "header": {
    "parameterNumberName": "northward_wind",
    "parameterUnit": "m.s-1",
    "parameterNumber": 3,
    "parameterCategory": 2,
    "nx": nx,
    "ny": ny,
    "numberPoints": tot,
    "dx": dx,
    "dy": dy,
    "la1": 90.0,
    "lo1": 0.0,
    "la2": -90.0,
    "lo2": 360.0,
    "refTime": "2017-02-01 23:00:00"
  },
  "data": v_data
}]


# In[25]:

# write JSON for leaflet-velocity input
with open('wind.json', 'w') as outfile:  
    json.dump(wind_data, outfile, separators=(',', ':'))


# In[26]:

# get data for temp from netCDF
temps = dataset.variables[temp_var][:][0]


# In[28]:

# get data for lat and lon
lats = dataset.variables['lat'][:]
lons = dataset.variables['lon'][:]


# In[29]:

# loop through and create array
# temp is scaled from Kelvin to 0-1 with range 200K to 350K
# USER can edit display options
temp_data = [[0,0,0] for i in range(len(lats) * len(lons))]
for i in range(len(lats)):
    for j in range(len(lons)):
        temp_data[j + (i * len(lons))][0] = lats[i]
        temp_data[j + (i * len(lons))][1] = lons[j]
        temp_data[j + (i * len(lons))][2] = (temps[i,j] - 273.15) # + 273.15 for K
        #temp_data[j + (i * len(lons))][2] = str((temps[i,j] - 200)/150) if string is necessary


# In[32]:

# apply non-overlapping moving window average to reduce data size by factor of 144 
# USER can edit grouping parameter
# number of points should not be more than several hundred for best performance
group = 12
lats_sm = lats.reshape(-1, group).mean(axis=1)
lons_sm = lons.reshape(-1, group).mean(axis=1)


# In[33]:

# create new smaller temperature array 
temp_array = [[0] for i in range(len(lats) * len(lons))]
for i in range(len(temp_data)):
    temp_array[i] = temp_data[i][2]
temps_sm = np.array(temp_array).reshape(-1, group * group).mean(axis=1)


# In[35]:

# reformat array to [lat, lon, temp]
temp_data_sm = [[0,0,0] for i in range(len(lats_sm) * len(lons_sm))]
for i in range(len(lats_sm)):
    for j in range(len(lons_sm)):
        temp_data_sm[j + (i * len(lons_sm))][0] = lats_sm[i]
        temp_data_sm[j + (i * len(lons_sm))][1] = lons_sm[j] -180
        temp_data_sm[j + (i * len(lons_sm))][2] = temps_sm[j + (i * len(lons_sm))] + 40


# In[36]:

# write Javascript file for Leaflet.idw input
with open('temps_sm.js', 'w') as filehandle:  
    filehandle.write('var addressPoints = ' + str(temp_data_sm))

