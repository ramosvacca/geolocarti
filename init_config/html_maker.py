def simple_markercircle(list_dict,name_to='test_sample'):

    pre = '''<!DOCTYPE html>
<html>
  <head>  <!-- www.techstrikers.com -->
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Geolocarti - SCOPUS </title>
    <style>
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #map {
        height: 99%;
        width:99%
      }
    </style>
        <script async defer
        src="https://maps.googleapis.com/maps/api/js?signed_in=true&callback=initMap"></script>
        <script>

// We create the variables needed.
          var map_zoom = 7
          var affiliations = '''
    post = '''
;

          var map_center = {lat:3.375709, lng:-76.532514};
          var aff_circles = [];

// We give title and content arguments, makeContent returns an html content built.
function makeContent(title,incont){

  var cont = '<div id="content">'+
  '<div id="siteNotice">'+
  '</div>'+
  '<h1 id="firstHeading" class="firstHeading">'+
  title+'</h1><p>'+incont+'</p>'+
  '</div>';

  return cont

};

// First, create an object containing LatLng and population for each city.
// Make a function to create the circles.

function initMap() {

  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: map_zoom,
    center: map_center,
    mapTypeId: google.maps.MapTypeId.TERRAIN
  });

  function makeCircle(affil_dict){

    var Latlng = {lat: affil_dict.lat, lng:affil_dict.lng};

    var infowindow = new google.maps.InfoWindow({
      maxWidth: 200,
      content: makeContent(affil_dict.Name, affil_dict.Content)
    });

    var thisCircle = new google.maps.Circle({
      strokeColor: '#FF0000',
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: '#FF0000',
      fillOpacity: 0.35,
      map: map,
      center: Latlng,
      radius: affil_dict.Radio,
      draggable:true
    });

    var marker = new google.maps.Marker({
          position: Latlng,
          map: null,
        });

    var initzoom = map.getZoom();

    if (initzoom < affil_dict.Zoom){
    thisCircle.setMap(null);
    marker.setMap(map)
    }
    else{
    thisCircle.setMap(map);
    marker.setMap(null)
    };

    google.maps.event.addListener(thisCircle, 'click', function(ev){
    infowindow.setPosition(thisCircle.getCenter());
    infowindow.open(map);
    });

    google.maps.event.addListener(thisCircle, 'mouseout', function(ev){
    infowindow.close();
    });

    google.maps.event.addListener(marker, 'click', function(ev1){
    infowindow.setPosition(marker.getPosition());
    infowindow.open(map);
    });

    google.maps.event.addListener(marker, 'mouseout', function(ev1){
    infowindow.close();
    });

    google.maps.event.addListener(map, 'zoom_changed', function(ev_z){

    var zoomnow = map.getZoom();

    if (zoomnow < affil_dict.Zoom){

      thisCircle.setMap(null);
      marker.setMap(map);

    }

    else {

      thisCircle.setMap(map);
      marker.setMap(null);

    }

    });

    aff_circles.push(thisCircle);

  };

  for (i = 0; i < affiliations.length; i++) {

    makeCircle(affiliations[i])

  };

}
    </script>
  </head>
  <body>
    <div id="map"></div>
  </body>
</html>'''

    final = pre + str(list_dict) + post

    filesaved = open('maps/'+name_to+'.html', 'W+')

    filesaved.write(final)