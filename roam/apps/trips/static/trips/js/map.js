const map = L.map("map").setView([20, 0], 2);
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);
const countriesLayer = L.geoJSON(null, {
    style: feature => {
        const properties = feature.properties || {};
        const code = properties["ISO3166-1-Alpha-2"] || properties["ISO_A2"] || properties["iso_a2"];
        const visitedCountries = window.visitedCountries || [];
        return {
            fillColor: visitedCountries.includes(code) ? "#22c55e" : "#e5e7eb",
            fillOpacity: 0.8,
            color: "#ffffff",
            weight: 1
        };
    }
}).addTo(map);

fetch("/trips/map/data/").then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error : ${response.status}`);
    }
    return response.json();
}).then(data => {
    window.visitedCountries = data.visited_countries || [];
    return fetch("https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson");
}).then(response => {
    if (!response.ok) {
        throw new Error("Error while loading GeoJSON");
    }
    return response.json();
}).then(geojson => {
    countriesLayer.addData(geojson);
    countriesLayer.setStyle(countriesLayer.options.style);
}).catch(error => console.error("Map error :", error));
