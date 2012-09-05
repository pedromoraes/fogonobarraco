function trace() {
	var args = Array.prototype.slice.call(arguments);
	if (window.console != undefined) console.log(args);
}

var map, Engine = function() {
	var items, markers = [], infoWindow, sheetID = '', basePath = '/', occurrencesCall = 'static/occurrences.json';
	return {
		init: function() {
			this.load();
			$("section#filters ul#years input").change(this.filterMarkers.bind(this));
			return this;
		},
		load: function() {
			$.getJSON(basePath+occurrencesCall, function(data) {
				if (data.success) {
					items = data.occurrences;
					this.createMarkers();
				} else {
					trace('error loading data', data);
				}
			}.bind(this)).error(trace);
		},
		filterMarkers: function() {
			markers.forEach(function(el) {
				if (el && el.data && el.data.date) {
					var year = el.data.date.split('/').pop(),
						active = $("section#filters ul#years input[value=\""+year+"\"]").attr('checked') ? true : false;
					el.setMap(active?map:null);
				}
			});
		},
		removeMarkers: function() {
			markers.forEach(function(el) {
				el.setMap(null);
			});
			markers = [];
		},
		createMarkers: function() {
			this.removeMarkers();
			items.forEach(function(item) {
				item.links = item.links.map(function(el,i) { return '<a href="'+el+'" target="_blank">'+(i+1)+'</a>'; }).join(', ');
				var marker = new google.maps.Marker({
					position: new google.maps.LatLng(item.coords[0], item.coords[1]),
					map: map,
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
				markers.push(marker);
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
