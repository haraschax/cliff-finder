const {DeckGL, TerrainLayer, IconLayer, ScatterplotLayer, _TerrainExtension, GeoJsonLayer} = deck;


const DATA_URL = "./data/cliffs_v2.csv";
const data = (await d3.csv(DATA_URL));


const elevationData = 'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png';
const elevationDecoder = {
  rScaler: 256,
  gScaler: 1,
  bScaler: 1 / 256,
  offset: -32768
};


// const texture = 'https://basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
// const texture = "https://basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"


// const texture = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}"
// const texture = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}"
const texture = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"


const terLayer = new TerrainLayer({
  id: 'terrain-source',
  elevationData: elevationData,
  elevationDecoder: elevationDecoder,
  texture: texture,
  maxZoom: 14,
  material: {
    diffuse: 1
  },
  operation: 'terrain+draw',
});


const scatLayer = new ScatterplotLayer({
    data: data,
    getPosition: (d) => {
      const lat = parseFloat(d.latitude);
      const lng = parseFloat(d.longitude);
      return [lng, lat];
    },
    getRadius: d => 500,

    pickable: true,
    autoHighlight: true,
    highlightColor: [241, 196, 15, 220],
    getFillColor: [192, 57, 43, 255],
    filled: true,
    stroked: true,
    getLineWidth: 2,
    lineWidthUnits: 'pixels',
    getLineColor: [255, 255, 255, 255],
    radiusMinPixels: 15,
    extensions: [new _TerrainExtension()],
    terrainDrawMode: 'drape'
  })


const deckgl = new DeckGL({
  initialViewState: {
    longitude: 0,
    latitude: 0,
    zoom: 1,
    maxZoom: 13,
    pitch: 0,
    bearing: 0
  },
  controller: true,
  layers: [terLayer, scatLayer],
  getTooltip: ({ object }) => object && {html: `<div>
  <p>Cliff Height: ${Math.round(parseFloat(object.height) * 100)/100}m</p>
  <p>Lat, Lng: ${Math.round(parseFloat(object.latitude) * 100) / 100}, ${Math.round(parseFloat(object.longitude) * 100)/100}</p>
  <p>(Click to view on Google Maps)</p>
  </div>`},
  onClick: ({object}) => {
    if (object) {
      const url = `https://www.google.com/maps/@${parseFloat(object.latitude)},${parseFloat(object.longitude)},10000m/data=!3m1!1e3?entry=ttu`;
      console.log(url);
      window.open(url)
    }
  }
});
