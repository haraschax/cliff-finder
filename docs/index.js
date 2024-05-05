//This example renders a scatterplot with DeckGL, on top of a basemap rendered with maplibre-gl, using a map style JSON from Carto.
const {DeckGL, ScatterplotLayer} = deck;


const DATA_URL = "./data/cliffs_v1.csv";

const data = (await d3.csv(DATA_URL));

console.log(data);



new DeckGL({
  mapStyle: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
  initialViewState: {
    longitude: 0,
    latitude: 0,
    zoom: 1
  },
  controller: true,
  layers: [
    new ScatterplotLayer({
      data: data,
      getPosition: (d) => {
        const lat = parseFloat(d.latitude);
        const lng = parseFloat(d.longitude);
        return [lng, lat];
      },
      getFillColor: d => [192, 57, 43, 255],
      getRadius: d => 100000,
      pickable: true,
      autoHighlight: true,
      highlightColor: [241, 196, 15, 220]
    })
  ],
  getTooltip: ({ object }) => object && `Cliff Height: ${Math.round(parseFloat(object.height), 2)}m`
});