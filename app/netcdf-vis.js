// Load Leaflet map

function initDemoMap(){

    var Esri_WorldImagery = L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: ''
    });

    //var OpenStreetMap_Mapnik = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    	//maxZoom: 19,
    	//attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    //});

    var Esri_DarkGreyCanvas = L.tileLayer(
        "http://{s}.sm.mapstack.stamen.com/" +
        "(toner-lite,$fff[difference],$fff[@23],$fff[hsl-saturation@20])/" +
        "{z}/{x}/{y}.png",
        {
            attribution: ''
        }
    );
    var attribution = 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, ' +
    'NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community';

    var baseLayers = {
        "Grey Canvas": Esri_DarkGreyCanvas,
        "Satellite": Esri_WorldImagery,
    };


    // set map bounds
    var corner1 = L.latLng(-89.98155760646617, -180.0),
    corner2 = L.latLng(89.99346179538875, 180.0),
    bounds = L.latLngBounds(corner1, corner2);

    var map = L.map('map', {
        layers: [ Esri_DarkGreyCanvas ],
        center: bounds.getCenter(),
        zoom: 10,
        minZoom: 2,
        maxZoom: 5,
        maxBounds: bounds,
        maxBoundsViscosity: 1
    });

    // layer control panal
    var layerControl = L.control.layers(baseLayers,null,{collapsed:false});
    layerControl.addTo(map);
    map.setView([0, 0], 1);

    // idw-map
    var idw = L.idwLayer(addressPoints,{
            opacity: 0.3,
            maxZoom: 18,
            cellSize: 5,
            exp: 3,
            max: 75
        })
        //idw.addTo(map);
    layerControl.addOverlay(idw, 'Global Temp').addTo(map)
    //L.control.layers(overlays,null,{collapsed:false}).addTo(map);

    return {
        map: map,
        layerControl: layerControl
    };

}

// demo map
var mapStuff = initDemoMap();
var map = mapStuff.map;
var layerControl = mapStuff.layerControl;

// load data (u, v grids) from somewhere (e.g. https://github.com/danwild/wind-js-server)
// try out a new json layer
$.getJSON('data/wind.json', function (data) {

	var velocityLayer = L.velocityLayer({
		displayValues: true,
		displayOptions: {
			velocityType: 'Wind',
			displayPosition: 'bottomleft',
			displayEmptyString: 'No wind data'
		},
		data: data,
		maxVelocity: 25
	});

	layerControl.addOverlay(velocityLayer, 'Global Wind');
});
