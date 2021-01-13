# netcdf-vis

`netcdf-vis` is a web application that extracts netCDF data and visualises it on a web map.

Live demo: [https://smlum.github.io/netcdf-vis/app/](https://smlum.github.io/netcdf-vis/app/)


## Using the app

The app provides users with an interactive Leaflet web map with temperature and wind data overlays.

The overlays and basemaps can be toggled from a control panel in the top right.


## Building and launching

Clone the netcdf-vis repository <br>
```
git clone https://github.com/samFredLumley/netcdf_vis
cd netcdf-vis/app
```
The app must be run on a web server. For example, using [http-server](https://www.npmjs.com/package/http-server):  
```
http-server
```
And then in your browser go to:
```
http://127.0.0.1:8081
```

## Custom netCDF data

To configure the app for custom netCDF data you must add the netCDF file to the `data/netcdf` directory and edit `data/netcdf2.py`.

It may be preferable to work with the IPython Notebook file `netcdf2leaflet-velocity.ipynb` to use the step-by-step commented instructions. For example, using [Jupyter Notebook](http://jupyter.org/) run:
```
cd netcdf-vis/app/data
jupyter notebook netcdf2leaflet-velocity.ipynb
```
Running the python file will generate two files: `wind.json` and `temps_sm.js`, which are used as inputs for the web map.

## Map configuration

The Leaflet map can be modified in `netcdf-vis.js`. Modifications to the Leaflet plugins can be made in the `src` and `dist` directories.

## Distribution

The demo app can be embedded into another webpage as an iframe:

``<iframe src="https://samfredlumley.github.io/netcdf-vis/app/" width="600" height="400"></iframe>``

A custom version of the app could be embedded in a similar way.

## References

This project relies on:
* [netCDF4](http://unidata.github.io/netcdf4-python/)
* [leaflet-velocity](https://github.com/danwild/leaflet-velocity)
* [Leaflet.idw](https://github.com/JoranBeaufort/Leaflet.idw)

Which themselves rely on:
* [L.CanvasOverlay.js](https://gist.github.com/Sumbera/11114288)
* [Leaflet.heat](https://github.com/Leaflet/Leaflet.heat)
* [earth](https://github.com/cambecc/earth)

## Further work
* Add instructions
* Create user interface for netCDF extraction
* Automate server side Python data processing from web app
* Integrate [netCDF conventions](https://www.unidata.ucar.edu/software/netcdf/conventions.html)
* Support time dimension
* Support data streaming
* Explore other temperature visualisation options
