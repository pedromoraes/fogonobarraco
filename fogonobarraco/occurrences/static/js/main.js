function trace() {
	var args = Array.prototype.slice.call(arguments);
	if (window.console != undefined) console.log(args);
}

var map, Engine = function() {
	var items, fireMarkers = [], infoWindow, sheetID = '', basePath = '/', occurrencesCall = 'static/occurrences.json',
		fireMarkerImage = new google.maps.MarkerImage('/static/img/fire-marker/image.png',new google.maps.Size(48,48),new google.maps.Point(0,0),new google.maps.Point(24,48)),
		fireMarkerShadow = new google.maps.MarkerImage('/static/img/fire-marker/shadow.png',new google.maps.Size(76,48),new google.maps.Point(0,0),new google.maps.Point(24,48)),
		fireMarkerShape = { coord: [14,0,15,1,16,2,17,3,19,4,21,5,28,6,30,7,31,8,33,9,33,10,34,11,35,12,36,13,36,14,37,15,37,16,38,17,38,18,38,19,40,20,40,21,40,22,40,23,40,24,41,25,41,26,41,27,41,28,41,29,41,30,41,31,41,32,41,33,41,34,40,35,40,36,40,37,39,38,39,39,38,40,37,41,36,42,35,43,33,44,32,45,29,46,19,46,16,45,14,44,12,43,11,42,10,41,9,40,8,39,8,38,7,37,7,36,7,35,6,34,6,33,6,32,6,31,6,30,6,29,6,28,6,27,6,26,8,25,8,24,8,23,8,22,8,21,8,20,8,19,8,18,9,17,9,16,10,15,11,14,12,13,17,12,17,11,17,10,16,9,16,8,15,7,15,6,14,5,14,4,14,3,13,2,13,1,13,0,14,0], type: 'poly' },
		chartMarkerImage = new google.maps.MarkerImage('/static/img/chart-marker/image.png',new google.maps.Size(64,64),new google.maps.Point(0,0),new google.maps.Point(32,64)),
		chartMarkerShadow = new google.maps.MarkerImage('/static/img/chart-marker/shadow.png',new google.maps.Size(100,64),new google.maps.Point(0,0),new google.maps.Point(32,64)),
		chartMarkerShape = { coord: [51,0,53,1,53,2,54,3,54,4,54,5,54,6,54,7,54,8,54,9,54,10,54,11,54,12,54,13,54,14,54,15,54,16,54,17,54,18,54,19,54,20,54,21,54,22,54,23,54,24,54,25,54,26,54,27,54,28,54,29,54,30,54,31,54,32,54,33,54,34,54,35,54,36,54,37,54,38,54,39,54,40,54,41,54,42,54,43,54,44,54,45,54,46,54,47,54,48,54,49,54,50,54,51,54,52,56,53,57,54,57,55,56,56,55,57,53,58,50,59,48,60,47,61,45,62,44,63,37,63,34,62,30,61,27,60,23,59,20,58,16,57,13,56,9,55,6,54,4,53,4,52,4,51,6,50,6,49,6,48,6,47,6,46,6,45,7,44,9,43,10,42,10,41,10,40,10,39,11,38,11,37,11,36,11,35,11,34,11,33,11,32,11,31,11,30,11,29,11,28,11,27,11,26,11,25,11,24,11,23,11,22,11,21,11,20,11,19,11,18,11,17,11,16,11,15,11,14,11,13,11,12,11,11,11,10,11,9,11,8,11,7,11,6,11,5,11,4,11,3,11,2,11,1,11,0,51,0], type: 'poly' };

	return {
		init: function() {
			this.loadOcurrences();
			$("section#filters ul#years input").change(this.filterFireMarkers.bind(this));
			return this;
		},
		loadOcurrences: function() {
			$.getJSON(basePath+occurrencesCall, function(data) {
				if (data.success) {
					items = data.occurrences;
					this.createFireMarkers();
				} else {
					trace('error loading data', data);
				}
			}.bind(this)).error(trace);
		},
		filterFireMarkers: function() {
			fireMarkers.forEach(function(el) {
				if (el && el.data && el.data.date) {
					var year = el.data.date.split('/').pop(),
						active = $("section#filters ul#years input[value=\""+year+"\"]").attr('checked') ? true : false;
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
			items.forEach(function(item) {
				item.links = item.links.map(function(el,i) { return '<a href="'+el+'" target="_blank">'+(i+1)+'</a>'; }).join(', ');
				var marker = new google.maps.Marker({
					position: new google.maps.LatLng(item.coords[0], item.coords[1]),
					map: map, icon: fireMarkerImage, shadow: fireMarkerShadow, shape: fireMarkerShape,
					title: item.slum_name
				});
				marker.data = item;
				google.maps.event.addListener(marker, 'click', function() {
					if (infoWindow) infoWindow.close();
					var content = '<div><dl><dt><strong>'+item.date+' - '+item.slum_name+'</strong></dt>',
						data = [['Endere&ccedil;o', 'location'],['Popula&ccedil;&atilde;o', 'population'],['Moradias destru&iacute;das', 'destroyed'],['Desabrigados', 'homeless'],
							['V&iacute;timas fatais', 'deaths'], ['Links', 'links'], ['Obs.', 'obs']];
					data.forEach(function(info) {
						content += '<dt>'+info[0]+':</dt><dd>'+item[info[1]]+'</dd>';
					});
					content += '</dl></div>';
		 			infoWindow = new google.maps.InfoWindow({content: content});
					infoWindow.open(map,marker);
				});
				fireMarkers.push(marker);
			});
		}
	}.init();
}

function initialize() {
	var mapOptions = {
		zoom: 12,
		center: new google.maps.LatLng(-23.550785,-46.634175),
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
	engine = new Engine();
}
google.maps.event.addDomListener(window, 'load', initialize);
