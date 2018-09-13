$(document).ready(function() {
  $('#example').DataTable( {
    "processing": true,
    "ajax" : {
      "url": "http://212.201.46.76:8080/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typename=planet:mars_paper&outputFormat=json",
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




/*


$(document).ready( function() {
  $('#example').dataTable( {
    "bProcessing"properties": false,
    "bServerSide"properties": true,
    "crossDomain"properties": true,
    "sAjaxSource"properties": "https://api.adsabs.harvard.edu/v1/search/query?q=Canberra&keyword=mars&fl=bibcode,title,author,year,pub,citation_count",
    "fnServerData"properties": function ( sSource, aoData, fnCallback, oSettings ) {
      oSettings.jqXHR = $.ajax( {
        "headers"properties":{
          "accept"properties": "application/json",
          "Authorization"properties": "Bearer " + "8Fq3szZtG7w8RBzHLq2broVHRS3pE6Ns0oEwv9WW",
          "Access-Control-Allow-Origin"properties": '*', 
          "Access-Control-Allow-Headers"properties": 'Content-Type'  
        },  
        "dataType"properties": 'json',
        "type"properties": "POST",
        "url"properties": sSource,
        "data"properties": aoData,
        "success"properties": fnCallback,
      });
    }
  });
});

*/


/*

        "headers"properties":{"Authorization"properties": "Bearer " + "8Fq3szZtG7w8RBzHLq2broVHRS3pE6Ns0oEwv9WW"},  
        "dataType"properties": 'json',
        "contentType"properties": "application/json",
        "Access-Control-Allow-Origin"properties": '*', 
        "Access-Control-Allow-Headers"properties": 'Content-Type',
        "type"properties": "POST",
        "url"properties": sSource,
        "data"properties": JSON.stringify(aoData),
        "success"properties": fnCallback,



"headers"properties":{
          'Authorization': "Bearer ","8Fq3szZtG7w8RBzHLq2broVHRS3pE6Ns0oEwv9WW"
        }


        "beforeSend"properties": function(xhr){
          xhr.setRequestHeader("Authorization" , "Bearer:8Fq3szZtG7w8RBzHLq2broVHRS3pE6Ns0oEwv9WW")},    

*/