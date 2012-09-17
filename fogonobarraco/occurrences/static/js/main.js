function trace() {
	var args = Array.prototype.slice.call(arguments);
	if (window.console != undefined) console.log(args);
}

var map;

function convertPoint(latLng) { 
	var topRight = map.getProjection().fromLatLngToPoint(map.getBounds().getNorthEast());
	var bottomLeft=map.getProjection().fromLatLngToPoint(map.getBounds().getSouthWest()); 
	var scale = Math.pow(2,map.getZoom()); 
	var worldPoint=map.getProjection().fromLatLngToPoint(latLng); 
	return new google.maps.Point((worldPoint.x-bottomLeft.x)*scale,(worldPoint.y-topRight.y)*scale); 
} 

var Engine = function() {
	var items, regions, indices, fireMarkers = [], regionsGeometries = [], indicesMarkers = [], fireInfoWindow, regionInfoWindow, sheetID = '', basePath = '/', occurrencesCall = 'occurrences.json', indexedRegionsCall = 'regions.json', regionsCall = 'static/distritos.json',
		indicesCall = "region/[id]/indices.json", slumsKml, 
		slumsCall = 'static/favelas.json', slumsGeometries = [],
		fireMarkerImage = new google.maps.MarkerImage('/static/img/fire-marker/image.png',new google.maps.Size(32,32),new google.maps.Point(0,0),new google.maps.Point(16,32)),
		fireMarkerShadow = new google.maps.MarkerImage('/static/img/fire-marker/shadow.png',new google.maps.Size(76,48),new google.maps.Point(0,0),new google.maps.Point(24,48)),
		fireMarkerShape = { coord: [10,0,10,1,12,2,14,3,19,4,21,5,22,6,23,7,23,8,24,9,25,10,25,11,25,12,26,13,27,14,27,15,27,16,27,17,27,18,27,19,27,20,27,21,27,22,27,23,27,24,26,25,26,26,25,27,24,28,23,29,21,30,20,31,11,31,10,30,8,29,7,28,6,27,5,26,5,25,4,24,4,23,4,22,4,21,4,20,4,19,4,18,4,17,5,16,5,15,5,14,5,13,5,12,5,11,6,10,7,9,8,8,11,7,11,6,10,5,9,4,9,3,9,2,8,1,8,0,10,0], type: 'poly' },
		chartMarkerImage = new google.maps.MarkerImage('/static/img/chart-marker/image.png',new google.maps.Size(32,32),new google.maps.Point(0,0),new google.maps.Point(16,32)),
		chartMarkerShadow = new google.maps.MarkerImage('/static/img/chart-marker/shadow.png',new google.maps.Size(52,32),new google.maps.Point(0,0),new google.maps.Point(16,32)),
		chartMarkerShape = { coord: [26,0,27,1,27,2,27,3,27,4,27,5,27,6,27,7,27,8,27,9,27,10,27,11,27,12,27,13,27,14,27,15,27,16,27,17,27,18,27,19,27,20,27,21,27,22,27,23,27,24,27,25,27,26,27,27,27,28,24,29,23,30,21,31,19,31,15,30,12,29,8,28,5,27,2,26,3,25,3,24,3,23,3,22,4,21,5,20,5,19,5,18,5,17,5,16,5,15,5,14,5,13,5,12,5,11,5,10,5,9,5,8,5,7,5,6,5,5,5,4,5,3,5,2,5,1,5,0,26,0], type: 'poly' },
		tooltip, 
		showTooltip = function(name, x, y) {
			if (tooltip) hideTooltip();
			tooltip = $('<div id="tooltip"></div>');
			tooltip.html(name);
			$('#map_canvas').prepend(tooltip);
			x -= tooltip.width() / 2;
			y -= tooltip.height() / 2 + 50;
			tooltip.css({marginLeft:x,marginTop:y});
		},
		hideTooltip = function() {
			if (tooltip) {
				$(tooltip).remove();
				tooltip = null;
			}
		};

	return {
		init: function() {
			this.loadOcurrences();
			this.loadIndices();
			this.loadRegions();
			this.loadSlums();
			$("section#filters ul#years input").change(this.filterFireMarkers.bind(this));
			$("section#filters ul#overlays input[name=\"cb_indices\"]").change(this.toggleIndicesMarkers.bind(this));
			$("section#filters ul#overlays input[name=\"cb_regions\"]").change(this.toggleRegionsLayer.bind(this));
			$("section#filters ul#overlays input[name=\"cb_slums\"]").change(this.toggleSlumsLayer.bind(this));
			return this;
		},
		loadOcurrences: function() {
			$.getJSON(basePath+occurrencesCall, function(data) {
				if (data.success) {
					items = data.occurrences.map(function(item) {
						for (var s in item) {
							switch (item[s]) {
								case -1:
								case "null":
								case null:
									item[s] = 'sem informa&ccedil;&atilde;o';
									break;
							}
						}
						return item;
					}); 
					this.createFireMarkers();
				} else {
					trace('error loading data', data);
				}
			}.bind(this)).error(trace);
		},
		loadIndices: function() {
			$.getJSON(indexedRegionsCall, function(data) {
				if (data.success) {
					indices = data.regions;
					this.createIndicesMarkers();
				} else {
					trace('error loading data', data);
				}
			}.bind(this)).error(trace);
		},
		loadRegions: function() {
			$.getJSON(regionsCall, function(data) {
				regions = data;
				regions.forEach(function(item) {
					var coords = $(item.geometria).text().split(' ');
					//trace(coords);
					var points = [];
					var bounds = new google.maps.LatLngBounds();
					coords.forEach(function(cs) {
						var parts = cs.split(','), latlng = new google.maps.LatLng(parts[1], parts[0]);
						points.push(latlng);
						bounds.extend(latlng);
					});
					var poly = new google.maps.Polygon({
						paths: points,
						strokeWeight: 1,
						strokeColor: '#f00',
						strokeOpacity: 0.5,
						fillColor: '#f00',
						fillOpacity: 0.05,
						cursor: 'default'
					});
					poly.bounds = bounds;
					google.maps.event.addListener(poly, 'mouseover', function() {
						this.setOptions({fillOpacity: 0.2, strokeColor: '#000'});
						var center = convertPoint(this.bounds.getCenter()), x = center.x, y = center.y;
						showTooltip(item.distrito, x, y);
					});
					google.maps.event.addListener(poly, 'mouseout', function(evt) {
						this.setOptions({fillOpacity: 0.05, strokeColor: '#f00'});
						if (evt.b.toElement != tooltip.get(0)) hideTooltip();
					});
					//poly.setMap(map);
					//trace(poly);
					//trace(bounds);
					regionsGeometries.push(poly);
				});
			}.bind(this)).error(trace);
		},
		loadSlums: function() {
			$.getJSON(slumsCall, function(data) {
				slums = data;
				slums.poly.forEach(function(item){
					var coords = item.coordenadas.split(' ');
					//trace(coords);
					var points = [];
					var bounds = new google.maps.LatLngBounds();
					coords.forEach(function(cs) {
						var parts = cs.split(','), latlng = new google.maps.LatLng(parts[1], parts[0]);
						points.push(latlng);
						bounds.extend(latlng);
					});
					var poly = new google.maps.Polygon({
						paths: points,
						strokeWeight: 1,
						strokeColor: '#A52A2A',
						strokeOpacity: 0.5,
						fillColor: '#A52A2A',
						fillOpacity: 0.5,
						cursor: 'default'
					});
					poly.bounds = bounds;
					
					//trace(item.favela);
					//trace(slums.favela[item.favela]);		
					
					google.maps.event.addListener(poly, 'mouseover', function() {
						this.setOptions({fillOpacity: 0.7, strokeColor: '#A52A2A'});
						var center = convertPoint(this.bounds.getCenter()), x = center.x, y = center.y;
						showTooltip('<strong>' + slums.favela[item.favela].nome.toUpperCase() + '</strong>' + "<br/>Pop. " + slums.favela[item.favela].populacao, x, y);
					});
					google.maps.event.addListener(poly, 'mouseout', function(evt) {
						this.setOptions({fillOpacity: 0.5, strokeColor: '#A52A2A'});
						if (evt.b.toElement != tooltip.get(0)) hideTooltip();
					});					
					//trace(bounds);
					slumsGeometries.push(poly);
				})
			}.bind(this)).error(trace);
		},
		toggleRegionsLayer: function() {
			var active = $("section#filters ul#overlays input[name=\"cb_regions\"]").attr('checked') ? true : false;
			regionsGeometries.forEach(function(el) { el.setMap(active?map:null); });
		},
		toggleSlumsLayer: function() {
			var active = $("section#filters ul#overlays input[name=\"cb_slums\"]").attr('checked') ? true : false;
			slumsGeometries.forEach(function(el) { el.setMap(active?map:null); });
		},		
		toggleIndicesMarkers: function() {
			var active = $("section#filters ul#overlays input[name=\"cb_indices\"]").attr('checked') ? true : false;
			indicesMarkers.forEach(function(el) { el.setMap(active?map:null); });
		},
		filterFireMarkers: function() {
			fireMarkers.forEach(function(el) {
				if (el && el.data) {
					var active = $("section#filters ul#years input[value=\""+el.data.year+"\"]").attr('checked') ? true : false;
					el.setMap(active?map:null);
				}
			});
		},
		removeFireMarkers: function() {
			fireMarkers.forEach(function(el) {
				el.setMap(null);
			});
			fireMarkers = [];
		},
		createFireMarkers: function() {
			this.removeFireMarkers();
			
			var urlEx = new RegExp(/(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gi);
			
			items.forEach(function(item) {
				item.links = item.evidences ? item.evidences.replace(urlEx,"<a href='$1' target='_blank'>$1</a>") : '';
				item.comments = item.comments ? item.comments.replace(urlEx,"<a href='$1' target='_blank'>$1</a>") : '';
				var marker = new google.maps.Marker({
					position: new google.maps.LatLng(item.latitude, item.longitude),
					map: map, icon: fireMarkerImage, shadow: fireMarkerShadow, shape: fireMarkerShape,
					title: item.slum_name
				});
				marker.data = item;
				google.maps.event.addListener(marker, 'click', function() {
					if (fireInfoWindow) fireInfoWindow.close();
					var content = '<div><dl><dt><strong>'+item.formatted_date+' - '+item.slum_name+'</strong></dt>',
						data = [['Endere&ccedil;o', 'location'],['Popula&ccedil;&atilde;o', 'population'],['Moradias destru&iacute;das', 'destroyed'],['Desabrigados', 'homeless'],
							['V&iacute;timas fatais', 'deaths'], ['Feridos', 'injured'], ['Links', 'links'], ['Obs.', 'comments']];
					data.forEach(function(info) {
						content += '<dt>'+info[0]+':</dt><dd>'+item[info[1]]+'</dd>';
					});
					content += '</dl></div>';
					fireInfoWindow = new google.maps.InfoWindow({content: content});
					fireInfoWindow.open(map,marker);
				});
				fireMarkers.push(marker);
			});
		},
		createIndicesMarkers: function() {
			indices.forEach(function(region) {
				var marker = new google.maps.Marker({
					position: new google.maps.LatLng(region.latitude, region.longitude),
					map: map, icon: chartMarkerImage, shadow: chartMarkerShadow, shape: chartMarkerShape,
					title: region.name
				});
				marker.data = region;
				google.maps.event.addListener(marker, 'click', function() {
					var content = '<div><p><strong>'+region.name+'</strong> - <a target="_blank" href="/chart/'+region.pk+'/?full=1">ampliar gr&aacute;fico</a></p>';
					content += '<iframe id="chart" frameborder=0 src="/chart/'+region.pk+'/" style="width: 300px; height: 200px;"></iframe>'
					content += '</div>';
					regionInfoWindow = new google.maps.InfoWindow({content: content});
					regionInfoWindow.open(map,marker);										
				});
				marker.setMap(map);
				indicesMarkers.push(marker);
			});
		}
	}.init();
}

function initialize() {
	var mapOptions = {
		zoom: 12,
		center: new google.maps.LatLng(-23.550785,-46.634175),
		mapTypeId: google.maps.MapTypeId.HYBRID
	};
	map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
	engine = new Engine();
}
google.maps.event.addDomListener(window, 'load', initialize);
