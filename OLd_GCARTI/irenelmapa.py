descr=['Santa_Marta', 'Colombia', 'Suramérica', 'Estados_Unidos', 'Suecia', 'Bogotá', 'Cundinamarca', 'Villavicencio', 'Australia', 'Distrito_Capital', 'Viena', 'Antioquia', 'Cartagena', 'Distrito_Federal_México', 'Bucaramanga', 'Cali', 'Suiza', 'Popayán', 'Indiana', 'Lyon', 'Brasil', 'Pasto', 'Tunja', 'Aguachica', 'Manizales', 'Latinoamérica', 'Dinamarca', 'La_Paz', 'Medellín', 'Chile', 'Barranquilla', 'Nigeria', 'Madrid', 'Venezuela', 'Francia', 'Valledupar', 'Alemania', 'Europa', 'India', 'Ecuador', 'México', 'Cauca']
lista=[[11.08615625, -73.90399929999998], [4.11566015, -72.93168349999999], [-19.24240005, -60.9736], [37.59999999999999, -95.665], [62.19833664999999, 17.5646052], [4.64829755, -74.107807], [4.78249555, -73.97070599999999], [4.110987, -73.46847245000001], [-27.9210555, 133.247866], [10.48262905, -66.98021949999999], [48.2206849, 16.3800599], [7.149886049999999, -75.5033395], [10.40014225, -75.507815], [19.3907336, -99.14361265000001], [7.165023, -73.10824494999999], [3.41059455, -76.58312205], [46.8131873, 8.22421005], [2.442695, -76.57840635], [39.7662195, -86.441277], [45.7579555, 4.835120949999999], [-14.2396023, -53.18050169999999], [1.052036, -77.20717454999999], [5.517352450000001, -73.37612444999999], [8.24796645, -73.62394119999999], [5.0741005, -75.5028765], [-11.71336855, -73.99785004999998], [56.15549105, 10.43308995], [-16.52071235, -68.0915129], [6.268678, -75.596392], [-36.7394323, -71.05658075000001], [10.9916034, -74.83900485], [9.077751, 8.677456999999999], [40.4379543, -3.67953665], [6.65711345, -66.61467055], [46.2157467, 2.20882575], [10.343651, -73.45780589999998], [51.16411754999999, 10.45411935], [49.5, 22.0], [21.13110835, 82.7792231], [-1.78646385, -78.13688744999999], [23.6266557, -102.53775015], [2.14486205, -76.98349409999999]]

import string
import os

def irenelmapa(lista, describe):

    describe = str(describe)

    listal=str(lista)

    a="""<!DOCTYPE html>  <html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Prueba de varios marcadores para VigTech</title>
    <style>
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #map {
        height: 100%;
      }
    </style>
  </head>
  <body>
	<div id="map"></div>
</div>

    <script>

function initMap() {
    var map;
    var bounds = new google.maps.LatLngBounds();
    var mapOptions = {
        mapTypeId: 'roadmap'
    };
                    
    // Display a map on the page
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
    map.setTilt(45);
        
    // Multiple Markers
    var markers = """+listal+""";
                        
    // Info Window Content
    var infoWindowContent = """+describe+""";
        
    // Display multiple markers on a map
    var infoWindow = new google.maps.InfoWindow(), marker, i;
    
    // Loop through our array of markers & place each one on the map  
    for( i = 0; i < markers.length; i++ ) {
        var position = new google.maps.LatLng(markers[i][1], markers[i][2]);
        bounds.extend(position);
        marker = new google.maps.Marker({
            position: position,
            map: map,
            title: markers[i][0]
        });
        
        // Allow each marker to have an info window    
        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
                infoWindow.setContent(infoWindowContent[i][0]);
                infoWindow.open(map, marker);
            }
        })(marker, i));

        // Automatically center the map fitting all markers on the screen
        map.fitBounds(bounds);
    }

    // Override our map zoom level once our fitBounds function runs (Make sure it only runs once)
    var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
        //this.setZoom(15);
        google.maps.event.removeListener(boundsListener);
    });
    
}

    </script>
    <script async defer
        src="http://maps.googleapis.com/maps/api/js?key=AIzaSyBYD6pcqIYZPIfy2-DwJbpHM_Lr1RwbfQk&signed_in=true&callback=initMap"></script>
  </body>
</html>"""
    return a

algo=irenelmapa(lista,descr)
path1 = os.path.abspath('Noviembre20.html')
f1 = open(path1, 'w')
f1.write(str(algo))