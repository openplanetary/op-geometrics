
  var base = new ol.layer.Tile({
      name: 'Basemap',
      source: new ol.source.XYZ({
      url: 'https://cartocdn-ashbu.global.ssl.fastly.net/nmanaud/api/v1/map/named/opm-mars-basemap-v0-1/0,1,2,3,4/{z}/{x}/{y}.png'
        })
      });

  var vectorSource = new ol.source.Vector({
          format: new ol.format.GeoJSON(),
          url: 'http://212.201.46.76:8080/geoserver/planet/wfs?service=WFS&version=2.0.0&request=GetFeature&typename=planet:mars_join&outputFormat=application/json',
          projection: 'EPSG:4326',
        });

  var vector = new ol.layer.Vector(
    { name: 'Feature Polygon',
      source: vectorSource
    });

  var unitsource = new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    url: 'http://212.201.46.76:8080/geoserver/planet/wfs?service=WFS&version=2.0.0&request=GetFeature&typename=planet:mars_units&outputFormat=application/json',
    projection: 'EPSG:4326'
  });

  var unit = new ol.layer.Vector(
    { name: 'Mars Units',
      source: unitsource
  });

  var popup = new ol.Overlay.Popup (
    { popupClass: "default anim", //"tooltips", "warning" "black" "default", "tips", "shadow",
      closeBox: true,
      onshow: function(){ console.log("You opened the box"); },
      onclose: function(){ console.log("You close the box"); },
      positioning: 'top-auto',
      autoPan: true,
      autoPanAnimation: { duration: 100 }
    });

  var map = new ol.Map
    ({
      target: 'map',
      view: new ol.View({
        center: [0, 0],
        zoom: 2,
        maxZoom: 17,
        minZoom: 2.7
        }),
      controls: ol.control.defaults().extend
      ([  new ol.control.LayerPopup(),
      ]),
      layers: [base, vector],
      overlays: [popup]
  });



  // Overlay
  var menu = new ol.control.Overlay ({ closeBox : true, className: "slide-left menu", content: $("#menu") });
  map.addControl(menu);

  // A toggle control to show/hide the menu
  var t = new ol.control.Toggle(
      { html: '<i class="fa fa-bars" ></i>',
        className: "menu",
        title: "Bibliographic Stats",
        onToggle: function() { menu.toggle(); }
      });
  map.addControl(t);


  //Control Select
  var select = new ol.interaction.Select({});
  map.addInteraction(select);

  var search = new ol.control.SearchFeature(
    { //target: $(".options").get(0),
      source: vectorSource, 
      property: 'name'
    });
  map.addControl (search);

  // Select feature when click on the reference index
  search.on('select', function(e)
    { select.getFeatures().clear();
      select.getFeatures().push (e.search);
      var p = e.search.getGeometry().getFirstCoordinate();
      map.getView().animate({ center:p });
    });


  // On selected => show/hide popup
  select.getFeatures().on(['add'], function(e)
  { var feature = e.element;
    var content = "";
    content += feature.get('name');
    content += '<br>';
    content += '-Type: ' + feature.get('feature_type');
    content += '<br>';
    content += '-Diameter: ' + feature.get('diameter');
    content += '<br>';
    content += '-Longitude: ' + feature.get('center_longitude');
    content += '<br>';
    content += '-Latitude: ' + feature.get('center_latitude');
    content += '<br>';
    content += '-Approval Date: ' + feature.get('approval_date');
    menu.show()
    popup.show(feature.getGeometry().getFirstCoordinate(), content); 
  })
  select.getFeatures().on(['remove'], function(e)
  { popup.hide(); 
    menu.hide();
  })

  select.getFeatures().on(['add'], function(e)
  {
    var feature = e.element;
    var tab = document.getElementById("publications");    
    $(document).ready(function() {
    $('#publications').DataTable( {
      "paging": false,
      "destroy": true,
      "order": [[0, "desc"]],
      "scrollY": 350,
      "processing": true,
      "ajax" : {
      "url": "http://212.201.46.76:8080/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typename=planet:mars_paper&outputFormat=json&CQL_FILTER=name=%27" + feature.get('name') + "%27",
      "dataSrc": "features"
    },
      "columns": [
        { "data" : "properties.citation_count" },
        { "data" : "properties.title" },
        { "data" : "properties.author" },
        { "data" : "properties.year" },
        { "data" : "properties.bibcode",
          "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
          $(nTd).html("<a href='https://ui.adsabs.harvard.edu/#abs/"+oData.properties.bibcode+"' target=_blank>"+oData.properties.bibcode+"</a>");
        }
    },
        { "data" : "properties.pub" }
    ] 
  });
});

  })


  select.getFeatures().on('add', function(e)
  { 
    var feature = e.element;

var dom = document.getElementById("chart");    
var myChart = echarts.init(dom);
var app = {};
option = null;
app.title = '堆叠条形图';

option = {
    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    legend: {
        data: ['-1970', '1971-1980','1981-1990','1991-2000','2001-2010','2011-2015', '2016-2018']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis:  {
        type: 'value'
    },
    yAxis: {
        type: 'category',
        data: ['Number of Papers','Number of Citing Papers','Number of Self-Citations','Total Number of Citations','Total Number of Referred Citations']
    },
    series: [
        {
            name: '-1970',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [feature.get("number_of_papers_1970"), feature.get("number_of_citing_papers_1970"), feature.get("number_of_self_citations_1970"), feature.get("total_number_of_citations_1970"), feature.get("total_number_of_refereed_citations_1970")]
        },
        {
            name: '1971-1980',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [feature.get("number_of_papers_1971_1980"), feature.get("number_of_citing_papers_1971_1980"), feature.get("number_of_self_citations_1971_1980"), feature.get("total_number_of_citations_1971_1980"), feature.get("total_number_of_refereed_citations_1971_1980")]
        },
        {
            name: '1981-1990',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [feature.get("number_of_papers_1981_1990"), feature.get("number_of_citing_papers_1981_1990"), feature.get("number_of_self_citations_1981_1990"), feature.get("total_number_of_citations_1981_1990"), feature.get("total_number_of_refereed_citations_1981_1990")]
        },
        {
            name: '1991-2000',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [feature.get("number_of_papers_1991_2000"), feature.get("number_of_citing_papers_1991_2000"), feature.get("number_of_self_citations_1991_2000"), feature.get("total_number_of_citations_1991_2000"), feature.get("total_number_of_refereed_citations_1991_2000")]
        },
        {
            name: '2001-2010',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [feature.get("number_of_papers_2001_2010"), feature.get("number_of_citing_papers_2001_2010"), feature.get("number_of_self_citations_2001_2010"), feature.get("total_number_of_citations_2001_2010"), feature.get("total_number_of_refereed_citations_2001_2010")]
        },
        {
            name: '2011-2015',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [feature.get("number_of_papers_2011_2015"), feature.get("number_of_citing_papers_2011_2015"), feature.get("number_of_self_citations_2011_2015"), feature.get("total_number_of_citations_2011_2015"), feature.get("total_number_of_refereed_citations_2011_2015")]
        },
        {
            name: '2016-2018',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [feature.get("number_of_papers_2016_2017"), feature.get("number_of_citing_papers_2016_2017"), feature.get("number_of_self_citations_2016_2017"), feature.get("total_number_of_citations_2016_2017"), feature.get("total_number_of_refereed_citations_2016_2017")]
        }

    ]
};;
if (option && typeof option === "object") {
    myChart.setOption(option, true);
}

    var content = "";
        content += feature.get('name');
        content += '<br>';
        content += feature.get('id');
 
    $(".data").html(content);
  });

  select.getFeatures().on('remove', function(e)
  { $(".data").html("");
  });