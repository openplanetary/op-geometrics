/* global Geocoder */
/*eslint strict: 0*/

(function (win, doc) {
  'use strict';
  var layers = [

      new ol.layer.Tile({
      source: new ol.source.XYZ({
      url: 'https://cartocdn-ashbu.global.ssl.fastly.net/nmanaud/api/v1/map/named/opm-mars-basemap-v0-1/0,1,2,3,4/{z}/{x}/{y}.png'
      })
    }),

      new ol.layer.Vector({
        source: new ol.source.Vector({
          format: new ol.format.WFS(),
          url: function (extent){
           return 'http://212.201.46.76:8080/geoserver/planet/wfs?service=WFS&' + 'version=2.0.0&request=GetFeature&typename=planet:mars_feature&' + 'outputFormat = application/jsonp' + extent.join(',');
         },
        })
      })
  ];

  var map = new ol.Map({
    layers: layers,
    target: 'map',
    view: new ol.View({
    center: [0, 0],
    zoom: 2,
    maxZoom: 17,
    minZoom: 2.8
      })
  });

  // Create an instance of the custom provider, passing any options that are
  // required
  var provider = OsOpenNamesSearch({
    url: 'http://212.201.46.76:8080/geoserver/wfs?service=WFS&version=1.0.0&request=GetFeature&typename=planet:mars_feature&outputFormat=application/json'
  });

  var geocoder = new Geocoder('nominatim', {
    // Specify the custom provider instance as the "provider" value
    provider: provider,
    autoComplete: true,
    autoCompleteMinLength: 2,
    targetType: 'text-input',
    lang: 'en',
    keepOpen: false,
    preventDefault: true
  });
  map.addControl(geocoder);

 geocoder.on('addresschosen', function (evt) {
    if (evt.bbox) {
      map.getView().fit(evt.bbox, { duration: 500 });
    } else {
      map.getView().animate({ zoom: 14, center: evt.coordinate });
    }
  });

  /**
   * Custom provider for OS OpenNames search covering Great Britian.
   * Factory function which returns an object with the methods getParameters
   * and handleResponse called by the Geocoder
   */
  function OsOpenNamesSearch(options) {
    var url = options.url;
    return {
      /**
       * Get the url, query string parameters and optional JSONP callback
       * name to be used to perform a search.
       * @param {object} options Options object with query, key, lang,
       * countrycodes and limit properties.
       * @return {object} Parameters for search request
       */
      getParameters: function (opt) {
        return {
          url: url,
          callbackName: 'callback',
          params: {
            q: opt.query
          }
        };
      },
      /**
       * Given the results of performing a search return an array of results
       * @param {object} data returned following a search request
       * @return {Array} Array of search results
       */
      handleResponse: function (results) {
        // The API returns a GeoJSON FeatureCollection
        if (results && results.features && results.features.properties.name) {
          return results.features.map(function (feature) {
            return {
              lon: features.properties.center_longitude,
              lat: features.properties.center_latitude,
              name: features.properties.name,
            };
          });
        } else {
          return;
        }
      }
    };
  }

})(window, document);