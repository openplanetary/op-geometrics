
var styleCache={};
	
	function getFeatureStyle (feature, sel)
	{	var k = $("#graph").val()+"-"+ $("#color").val()+"-"+(sel?"1-":"")+feature.get("data");
  		var style = styleCache[k];
		if (!style) 
		{	var radius = 15;
			// area proportional to data size: s=PI*r^2
			radius = 8* Math.sqrt (feature.get("sum") / Math.PI);
			var data = feature.get("data");
			radius *= (sel?1.2:1);
			// Create chart style
			style = [ new ol.style.Style(
				{	image: new ol.style.Chart(
					{	type: "pie", 
						radius: radius, 
						data: data, 
						rotateWithView: true,
						stroke: new ol.style.Stroke(
						{	color: "#fff",
							width: 2
						}),
					})
				})];

			// Show values on select
			if (sel)
			{	/*
				var sum = 0;
				for (var i=0; i<data.length; i++)
				{	sum += data[i];
				}
				*/
				var sum = feature.get("sum");
      
				var s = 0;
				for (var i=0; i<data.length; i++)
				{	var d = data[i];
      				var a = (2*s+d)/sum * Math.PI - Math.PI/2; 
					var v = Math.round(d/sum*1000);
					if (v>0)
      				{	style.push(new ol.style.Style(
						{	text: new ol.style.Text(
							{	text: (v/10)+"%", /* d.toString() */
          						offsetX: Math.cos(a)*(radius+3),
          						offsetY: Math.sin(a)*(radius+3),
								textAlign: (a < Math.PI/2 ? "left":"right"),
								textBaseline: "middle",
								stroke: new ol.style.Stroke({ color:"#fff", width:2.5 }),
								fill: new ol.style.Fill({color:"#333"})
							})
						}));
					}
					s += d;
				}
			}
		}
		styleCache[k] = style;
		return style;
	}

		// 30 random features with data: array of 4 values
	var ext = map.getView().calculateExtent(map.getSize());
	var features=[];
	for (var i=0; i<30; ++i)
	{	var n, nb=0, data=[];
		for (var k=0; k<4; k++) 
		{	n = Math.round(8*Math.random());
			data.push(n);
			nb += n;
		}
		features[i] = new ol.Feature(
			{	geometry: new ol.geom.Point([ext[0]+(ext[2]-ext[0])*Math.random(), ext[1]+(ext[3]-ext[1])*Math.random()]),
				data: data,
				sum: nb
			});
	}