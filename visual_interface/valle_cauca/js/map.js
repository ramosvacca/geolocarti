 var aff_circles = [];
 var markers = [];
 links = [];
 var markersDict = {};

 var active_nodes = {};
 var radius_multiplier = 40;
 mainmap = [];
 heatmap = [];
base_HOST = window.location.hostname


 repo_name = 'virtual_sep17'
 baseUrl_query = 'http://'+base_HOST+':10035/repositories/'+repo_name+'/sparql?query='


launcher = function () {
 const map_launcher = setInterval(function () {
    //console.log('debug')
    //console.log(results.length)
    //console.log(counter)
        if (typeof affiliations != 'undefined') { //It returns a list of affiliations ids
        maptolaunch()
        clearInterval(map_launcher)
    }
        }, 50);
};

maptolaunch = function () {

    function initial_info() {
        // This shows the html-element with the id "info" and adds the html content
        jQuery( '#info' ).empty();
        jQuery( '#info' ).show(1000);
        // This clears the content before you add new one
        jQuery( '#info' ).append(makeContent());

    };

    initial_info();

    mainmap = new google.maps.Map(document.getElementById('valle_cauca_map'), {
    zoom: map_zoom,
    center: map_center,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    styles:[
  {
    "featureType": "administrative",
    "stylers": [
      {
        "saturation": "-100"
      }
    ]
  },
  {
    "featureType": "administrative.land_parcel",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "administrative.neighborhood",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "administrative.province",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "landscape",
    "stylers": [
      {
        "saturation": -100
      },
      {
        "lightness": 25
      },
      {
        "visibility": "on"
      }
    ]
  },
  {
        "featureType": "landscape.natural.terrain",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "on"
            },
            {
                "lightness": "-100"
            }
        ]
    },
  {
    "featureType": "poi",
    "stylers": [
      {
        "saturation": -100
      },
      {
        "lightness": "50"
      },
      {
        "visibility": "simplified"
      }
    ]
  },
  {
    "featureType": "poi",
    "elementType": "labels.text",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "poi.business",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "road",
    "stylers": [
      {
        "saturation": "-100"
      }
    ]
  },
  {
    "featureType": "road",
    "elementType": "labels",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "road",
    "elementType": "labels.icon",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "road.arterial",
    "stylers": [
      {
        "lightness": "30"
      },
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "stylers": [
      {
        "visibility": "simplified"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "elementType": "labels",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "road.local",
    "stylers": [
      {
        "lightness": "40"
      },
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "transit",
    "stylers": [
      {
        "saturation": -100
      },
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "geometry",
    "stylers": [
      {
        "hue": "#ffff00"
      },
      {
        "saturation": -97
      },
      {
        "lightness": -25
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "labels",
    "stylers": [
      {
        "saturation": -100
      },
      {
        "lightness": -25
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "labels.text",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  }
]
    });

    testpoints = [new google.maps.LatLng(37.782551, -122.445368),
          new google.maps.LatLng(37.782745, -122.444586),
          new google.maps.LatLng(37.782842, -122.443688),
          new google.maps.LatLng(37.782919, -122.442815),
          new google.maps.LatLng(37.782992, -122.442112),
          new google.maps.LatLng(37.783100, -122.441461),
          new google.maps.LatLng(37.783206, -122.440829),
          new google.maps.LatLng(37.783273, -122.440324),
          new google.maps.LatLng(37.783316, -122.440023)]



    heatmap = new google.maps.visualization.HeatmapLayer({
          map: mainmap,
          opacity: 1,
          radius: 20,
          show: function(){this.setMap(mainmap)},
          hide: function(){this.setMap(null)},
        });


    var infowindow = new google.maps.InfoWindow({    });



    this.makeCircle = function (affil_dict){

        var image = {
            url: "../images/icons/edu.png",
            // This marker is 20 pixels wide by 32 pixels high.
            size: new google.maps.Size(32, 32),
            // The origin for this image is (0, 0).
            origin: new google.maps.Point(0, 0),
            // The anchor for this image is the base of the flagpole at (0, 32).
            anchor: new google.maps.Point(0, 32),
        };

        var affid = affil_dict.affid;

        var Latlng = {lat: locations[affid].lat, lng:locations[affid].lng};

         var infowindow = new google.maps.InfoWindow({
      maxWidth: 350

    });

    // NEXT CODE REPLACES INFOWINDOW BACKGROUND COLOR AND ROUNDS IT CORNERS
      google.maps.event.addListener(infowindow, 'domready', function() {

        // Reference to the DIV which receives the contents of the infowindow using jQuery
        var iwOuter = $('.gm-style-iw');

        var iwBackground = iwOuter.prev();
        // Remove the background shadow DIV
        iwBackground.children(':nth-child(2)').css({'display' : 'none'
        });

        // Remove the white background DIV
        iwBackground.children(':nth-child(4)').css(

        {'border' : '1.3px solid dodgerblue', 'background-color' : '#86E1FF', 'opacity': '.65'
        });

        iwBackground.children().css(

        {'border-radius':'12px'
        });

        var iwCloseBtn = iwOuter.next();

        // Apply the desired effect to the close button
        iwCloseBtn.css({
        'opacity': '0.65', // by default the close button has an opacity of 0.7
        'right': '2px', 'top': '2px', // button repositioning
        'border': '12px solid #48b5e9', // increasing button border and new color
        'border-radius': '50px', // circular effect
        'box-shadow': '0 0 5px #3990B9' // 3D effect to highlight the button
        });

        // The API automatically applies 0.7 opacity to the button after the mouseout event.
        // This function reverses this event to the desired value.
        iwCloseBtn.mouseover(function(){
          $(this).css({'opacity': '1'});
        });

        iwCloseBtn.mouseout(function(){
          $(this).css({'opacity': '0.65|'});
        });

      });



// NEXT CODE DEFINES THE CIRCLE ELEMENT
        var thisCircle = new google.maps.Circle({
            strokeColor: '#FF0000',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: '#FF0000',
            fillOpacity: 0.35,
            map: null,
            center: Latlng,
            radius: affil_dict.Radio * radius_multiplier,
            draggable:false,
            icon: image,
            title: affil_dict.final_id,
            zIndex: affil_dict['z-index'],
            cluster_info:'green436',
            fillColor: 'green',
            fillOpacity: 0.4,
            strokeColor: 'darkolivegreen',
            strokeWeight: 0.3,
            show: function(){this.setMap(mainmap)},
            hide: function(){this.setMap(null)},

        });

// NEXT CODE DEFINES THE MARKER ELEMENT


        var marker = new google.maps.Marker({
              position: Latlng,
              map: mainmap,
              icon: null,
              draggable: true,
              show: function(){this.setMap(mainmap)},
              hide: function(){this.setMap(null)},
              affid: affid,
              cluster: 0,
              weight: 0,
              active: false,
              tagged: false,
              tag_loc:'',
              tag_reg:'',
              tag_country:'',
              tag_code:'',
        });

        var initzoom = mainmap.getZoom();


        google.maps.event.addListenerOnce(mainmap, 'tilesloaded', function(rte) {
            // This pans the viewport/centers the marker in your viewport
            jQuery('#WaitDialog').hide(3000);


        } );


        google.maps.event.addListener( marker, 'rightclick', function() {
            // This pans the viewport/centers the marker in your viewport

            jQuery( '#info' ).empty();
            jQuery( '#info' ).append(makeContent(affil_dict));
            buttons_actions();

        } ); // Adds listener to

        google.maps.event.addListener( marker, 'click', function() {
            // This pans the viewport/centers the marker in your viewport

            infowindow.setPosition(marker.getPosition());
            infowindow.setContent(infowindowContent(affil_dict, marker.tag_loc, marker.tag_reg, marker.tag_country, marker.weight, marker.cluster));
            infowindow.open(mainmap, this);

        } ); // Adds listener to

        google.maps.event.addListener(thisCircle, 'click', function() {
            // This pans the viewport/centers the marker in your viewport

            jQuery( '#info' ).empty();
            jQuery( '#info' ).append(makeContent(affil_dict));
            buttons_actions();


        } );

        google.maps.event.addListener(thisCircle, 'rightclick', function() {
            // This pans the viewport/centers the marker in your viewport

            thisCircle.setMap(null);

        } );

// save all circle/markers on an array named aff_circles

        aff_circles.push(thisCircle);
        markers.push(marker);

    }; // AQUI TERMINA LA FUNCION CIRCLE MAKER


     function cleanAll() {


    uncheck_check(false,'links_chbx',links);
    uncheck_check(false,'circles_chbx',aff_circles);
    uncheck_check(false,'icons_chbx',markers);
    }; //hideAll on the screen


     this.uncheck_check = function (func, elemntId, list) {
        console.log(elemntId)

        var tosh = document.getElementById(elemntId);
        console.log(tosh);

        document.getElementById(elemntId).checked = func;
        _hideshow(list, elemntId)
    };  //changes option value depending on func. Then calls _hideshow
    // func is true to show or false to hide. elemntId is the element to change, list is the list to modify, show or hide.

     function _hideshow(list,elemntId){

       var checkbox = document.getElementById(elemntId);
       console.log(checkbox)

       if(checkbox.checked) {

           for (i = 0; i < list.length; i++) {
            list[i].setMap(mainmap)

            }
       }

       else {
            for (i = 0; i < list.length; i++) {
            list[i].setMap(null)
            }
        }

        }; // hides or show the total of element on each category depending on the option selected.

    // executes the function to create the circle/markers for each item dict on the list.

        for (i = 0; i < affiliations.length; i++) {

        makeCircle(affiliations[i])

       };


    for (var i = 0; i < markers.length; i++) {
                markersDict[markers[i].affid] = i
                }

    nodeTagger(); //tag markers with geo info.

    // Draws all the weighted links
        for(var link in weighted_links) {

            console.log(Object.keys(weighted_links).length + ' drawn links');

            var node_1_lat = locations[weighted_links[link].node1]['lat'];
            var node_1_lng = locations[weighted_links[link].node1]['lng'];
            var node_2_lat = locations[weighted_links[link].node2]['lat'];
            var node_2_lng = locations[weighted_links[link].node2]['lng'];


            var coords = [
            new google.maps.LatLng(node_1_lat, node_1_lng),
            new google.maps.LatLng(node_2_lat, node_2_lng)];
            var link_weight = weighted_links[link].weight/3;

            var my_line = new google.maps.Polyline({
                path: coords,
                map: mainmap,
                show: function(){this.setMap(mainmap)},
                hide: function(){this.setMap(null)},
                geodesic:true,
                strokeWeight:link_weight,
                strokeOpacity:0.4,
                strokeColor:'white',
                node_1: weighted_links[link].node1,
                node_2: weighted_links[link].node2,
                colorchecker: function () {return this.strokeColor},
                cluster:0,





            });
            links.push(my_line);
       };


    buttons_actions = function(){
    document.getElementById("icons_chbx").onchange = function () {_hideshow(markers,"icons_chbx")};
    document.getElementById("circles_chbx").onchange = function () {_hideshow(aff_circles,"circles_chbx")};
    document.getElementById('links_chbx').onchange = function () {_hideshow(links,'links_chbx')};

    document.getElementById('button_inRegion').onclick = function() {var queryType = 'allinRegion'; mainQuery(queryType)};
    document.getElementById('button_offRegion').onclick = function() {var queryType = 'outofRegion'; mainQuery(queryType)};
    document.getElementById('button_onRegion_offSubregion').onclick = function() {
    var queryType = 'inRegion_offSubregion'; mainQuery(queryType)};
    document.getElementById('button_offRegion_onSubregion').onclick = function() {
    var queryType = 'offRegion_inSubregion'; mainQuery(queryType)};

    document.getElementById('button_drawAll').onclick = function () {var queryType = 'countryNetwork'; mainQuery(queryType)};

    document.getElementById('node_country').onclick = function () {var queryType = 'nodeCountry'; mainQuery(queryType)};

    // CIRCLES CONTROLS
    document.getElementById('button_inCircle1').onclick = function() {var queryType = 'inCircle1'; circleQuery(queryType)};
    document.getElementById('button_offCircle1').onclick = function() {var queryType = 'offCircle1'; circleQuery(queryType)};
    document.getElementById('button_offCircle1_onCircle2').onclick = function() {
    var queryType = 'offCircle1_onCircle2'; circleQuery(queryType)};
    document.getElementById('button_onCircle1_offCircle2').onclick = function() {
    var queryType = 'onCircle1_offCircle2'; circleQuery(queryType)};

    document.getElementById('button_hideAll').onclick = function () {cleanAll()};
    document.getElementById('button_resetLinks').onclick = function () {resetLinks()};
    document.getElementById('button_activeLinks').onclick = function () {showactiveLinks()};
    document.getElementById('button_activeNodes').onclick = function () {activeNodes()};

    document.getElementById("button_statistics").onclick = function(){relationsDiscovery()};

    document.getElementById("button_clusterStatistics").onclick = function(){
        var cluster_number = parseInt(document.getElementById('clusterNumber').value)
        console.log(cluster_number)

        if (cluster_number == 0){
            relationsDiscovery(0)
        } else if (typeof cluster_number == 'number'){
            relationsDiscovery(cluster_number)
        }};

    document.getElementById("button_clusterheatmap").onclick = function(){activenodesHeatmap(true)};

    document.getElementById('button_clusterNodes').onclick = function () {activeNodes(0)};


    } // We need to initialize all the DOM functions... so we capture the events here to launche them from a button.

    buttons_actions();


    google.maps.event.addListener(mainmap, 'rightclick', function(algo) { //launches circlequery from where i have clicked the map.
            // This pans the viewport/centers the marker in your viewport
            var ext_lat = algo.latLng.lat()
            , ext_lon = algo.latLng.lng()
            , queryType = 'inCircle1'

            circleQuery(queryType, ext_lat, ext_lon)

        } );


};


//////////// MAP ENDS /////////////////
//                                  //
//                                  //
//                                  //
//////TERMINA MAPA ///////////////////
//                                  //
//                                  //
//                                  //
// TERMINA FUNCION MAP ///////////////


function circleQuery(queryType, ext_lat, ext_lon){
jQuery('#WaitDialog').show(50);
    console.log('starting circleQuery')
    var circle2_radius = document.getElementById("circle2_radius").value
    , circle1_radius = document.getElementById("circle1_radius").value;

    if (queryType == 'offCircle1_onCircle2' || queryType == 'onCircle1_offCircle2'){
        if (Number(circle1_radius) >= Number(circle2_radius)) {
        console.log(circle1_radius, circle2_radius)
        alert('Por favor revise el tamaño de las circunferencias'); return}
    }

    var affid = document.getElementById("scopus_id_tofind").textContent

    if (typeof ext_lat == 'undefined' && typeof ext_lon == 'undefined'){
        local_lat = locations[affid].lat;
        local_lon = locations[affid].lng; console.log(local_lat,local_lon, circle1_radius, circle2_radius)

    } else { local_lat = ext_lat;
    local_lon = ext_lon;
        }


        var sentQuery = sparql_circleQuery(affid, queryType, local_lat, local_lon, circle1_radius, circle2_radius)
        , url = baseUrl_query + encodeURIComponent(sentQuery)
        , getrequestDict  = {'var_return':'0'}
        , return_dict = get_request(url, 'GET', getrequestDict);



    console.log(url)

    const return_dictInterval = setInterval(function () {//We need a function to wait for th evalue of the return dict changes to true
    //so it can continue the execution.. on the other side there is a timer that changes the value to true
    // when all of the ids have been inserted into the list.
        if (return_dict[1] == true) {
            console.log(return_dict[1])
            console.log(return_dict[0]) //It returns a list of affiliations ids
            clearInterval(return_dictInterval)
            draw(affid, return_dict[0])
        } else {console.log('waiting')}
    }, 100);

}; //

function draw (affid, list) { //When we need to parse the return data from getrequest.. It can be one list
    //to paint the nodes related to me, then paint the links from the stored. It can be a list of two, so I paint the
    //nodes related to me with weight... or it can be a list of 3, Then I paint the 2 nodes in the list, either with weight or not..
    if (list.length == 0) {jQuery('#WaitDialog').hide(100);return}
    var look_for = document.getElementById('lookfor').value;

    console.log('inside draw')

    for (var i = 0; i < list.length; i++) {
        //console.log('inside i')
        for (var k = 0; k < markers.length; k++) {
            if (list[i][0]==markers[k].affid) {
                markers[k].show()
                markers[k].active = true
                markers[k].weight = parseInt(list[i][1])
                //console.log('markers done')
            }
        }

        for (var k_2 = 0; k_2 < links.length; k_2++){

            if ((list[i][0] == links[k_2].node_1 && affid == links[k_2].node_2) ||
             (list[i][0] == links[k_2].node_2 && affid == links[k_2].node_1) ) {

                //console.log('lloking for ook_for')
                if (look_for == 'references') {
                    if (links[k_2].colorchecker() == 'red') {
                    links[k_2].strokeColor = 'black'
                    } else if (links[k_2].colorchecker() == 'yellow') {
                    links[k_2].strokeColor = 'green'
                    } else if (links[k_2].colorchecker() == 'magenta') {
                    links[k_2].strokeColor = 'blue'
                    } else if (links[k_2].colorchecker() == 'white') {
                    links[k_2].strokeColor = 'cyan' }
                } else if (look_for == 'coauthorship')
                {
                    if (links[k_2].colorchecker() == 'green') {
                    links[k_2].strokeColor = 'black'
                    } else if (links[k_2].colorchecker() == 'yellow') {
                    links[k_2].strokeColor = 'red'
                    } else if (links[k_2].colorchecker() == 'cyan') {
                    links[k_2].strokeColor = 'blue'
                    } else if (links[k_2].colorchecker() == 'white') {
                    links[k_2].strokeColor = 'magenta'}
                } else if (look_for == 'citations')
                {
                    if (links[k_2].colorchecker() == 'cyan') {
                    links[k_2].strokeColor = 'green'
                    } else if (links[k_2].colorchecker() == 'blue') {
                    links[k_2].strokeColor = 'black'
                    } else if (links[k_2].colorchecker() == 'magenta') {
                    links[k_2].strokeColor = 'red'
                    } else if (links[k_2].colorchecker() == 'white') {
                    links[k_2].strokeColor = 'yellow' ;}
                }
                //console.log(k_2);
                //console.log('drawn __ H¡CHANGED')
            }
        }
    };
jQuery('#WaitDialog').hide(100);
};

function mainQuery(queryType) {// the main SPARQL query... to call the function that makes the http request.
    jQuery('#WaitDialog').show(50);
    var look_for = document.getElementById('lookfor').value;
    var start_year = document.getElementById('start_year').value;
    var final_year = document.getElementById('final_year').value;
    var code = document.getElementById('country_code').value;
    var getrequestDict  = {'var_return':'2'};
   console.log(queryType)

    var affid = document.getElementById("scopus_id_tofind").textContent
        , outer_region = document.getElementById("which_region").value
        , subRegion = document.getElementById("which_subRegion").value

    var local_dict = {'start_year': start_year, 'final_year': final_year}



    if (queryType == 'nodeCountry'){
            if (typeof arguments [1] != 'undefined'){
                affid = arguments[1]
                code = arguments[2]
                console.log('ADFASDF '+affid+code)

            }

        console.log('query type nodeCountry')
        local_dict.nodeCountry = true; local_dict.code = code;
        var sentQuery = sparqlQuery(affid, outer_region, queryType, subRegion, local_dict)
        var url = baseUrl_query + encodeURIComponent(sentQuery)

    } else if (queryType == 'countryNetwork') {
        getrequestDict['var_return'] = 1;
        var sentQuery = countrynodesQuery(code)
        , url = baseUrl_query + encodeURIComponent(sentQuery)
        console.log(url)

    } else
    {

        var sentQuery = sparqlQuery(affid, outer_region, queryType, subRegion, local_dict)
        var url = baseUrl_query + encodeURIComponent(sentQuery)
    }


    //console.log('var return  ', var_return)

    //var var_return = '0'

    var return_dict = get_request(url, 'GET', getrequestDict);
    console.log(url)

    const return_dictInterval = setInterval(function () {
            if (return_dict[1] == true) {
                console.log(return_dict[1])
                console.log(return_dict[0]) //It returns a list of affiliations ids
                clearInterval(return_dictInterval)
                if (queryType == 'countryNetwork'){
                    var checkbox = document.getElementById('betweenRegions');
                    if(checkbox.checked) {
                        code = document.getElementById('second_region_name').value
                    }
                    for (i = 0; i < return_dict[0].length ; i++) {//return_dict[0].length; i++) {
                        console.log('executing mainquery for each node and code' + return_dict[0][i] + code)


                        mainQuery('nodeCountry', return_dict[0][i][0], code)

                    }
                } else
                {
                    draw(affid, return_dict[0])
                }

            } else {console.log('waiting')}
        }, 100);

}; //termina Mainquery

function get_request (url, method, ...restDict){//, control_variable) {// This works with sparqlQuery
    if (method == 'GET') {
        var_return = restDict[0].var_return
    }

    console.log(typeof restDict[0])

    var return_array = [];
    console.log('starting get_request: ' + restDict[0].var_return)
    var results = ['a'];
    var counter = 0;
    var xmlHttp = new XMLHttpRequest();
        xmlHttp.open(method, url, true); // true for asynchronous
        //xmlHttp.setRequestHeader()
    xmlHttp.onload = function() {

    //console.log(xmlHttp.responseText)

    if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
        var list = false
        //console.log(xmlHttp)
        var respo = xmlHttp.responseText;
        //console.log(respo)
        var xmlDoc = $.parseXML( respo ), //XML parsed
        $xml = $( xmlDoc );
        results = $xml.find( "result" );
        console.log(results.length)

        //console.log(xmlDoc)
        //console.log(results)

        for (var i = 0; i < results.length; i++) {
            console.log(results[i])
            counter++;

            var html_affid = results[i].getElementsByTagName("binding")[0].getElementsByTagName('uri')[0].innerHTML;

            var regex_affid = /[0-9]+/i;

            var local_affid = html_affid.match(regex_affid)



            if (var_return == '1' || var_return =='0') {

                html_count = 'NOT COUNT REQUiRED'


                }

            else if (var_return == '2') {

                var html_count = results[i].getElementsByTagName("binding")[1].getElementsByTagName('literal')[0].innerHTML;
                console.log(html_count)

                } /*else if (var_return == '5') {

                var city = results[i].getElementsByTagName("binding")[1].getElementsByTagName('uri')[0].innerHTML;
                , region = results[i].getElementsByTagName("binding")[2].getElementsByTagName('uri')[0].innerHTML;
                , country = results[i].getElementsByTagName("binding")[3].getElementsByTagName('uri')[0].innerHTML;
                , code =results[i].getElementsByTagName("binding")[4].getElementsByTagName('uri')[0].innerHTML;

                }*/

            return_array.push([local_affid[0],html_count])

           // console.log(local_affid[0])

            };

        //console.log(return_array, counter);

        };

    };

    xmlHttp.send(null);

    const return_true = setInterval(function () {
    //console.log('debug')
    //console.log(results.length)
    //console.log(counter)
        if (results.length == counter) { //It returns a list of affiliations ids
            clearInterval(return_true)
            toreturn[1] = true;
    }
        }, 50);
//control_variable = true;
//console.log('before returning array: ' + control_variable);
    var toreturn = [return_array, false]

    return toreturn

};

function resetLinks () {
for (var i = 0; i < links.length; i++) {
            links[i].strokeColor = 'white'
            links[i].hide()
            links[i].show()
            };
            for (var i = 0; i < markers.length; i++) {
            markers[i].setIcon(null)
            markers[i].active = false
            markers[i].cluster = 0

};

} // Reset all links and all to 0

function activeNodes () {//shows active nodes, or cluster nodes.

    if (arguments[0] == 0) {

        for (var i = 0; i < markers.length; i++) {
                if (markers[i].cluster != 0){
                    markers[i].show()
                } else {
                markers[i].hide()
                }

        }
    } else if (typeof arguments[0] == 'number'){
        for (var i = 0; i < markers.length; i++) {
            if (markers[i].cluster == arguments[0]){
                markers[i].show()
            } else {

            markers[i].hide()}
        }
    } else {
        for (var i = 0; i < markers.length; i++) {
            if (markers[i].active){
                markers[i].show()
            } else {

            markers[i].hide()}
        }
    }


}; //Shows active nodes or cluster nodes.

function showactiveLinks () {

    for (var i = 0; i < links.length; i++) {
            if (links[i].strokeColor != 'white') {
            links[i].show()
            } else {links[i].hide()}
            };

} //shows active links.

function iconMaker (image_name) {
     toreturn = {url: `../images/icons/${image_name}`,
            // This marker is 20 pixels wide by 32 pixels high.
            size: new google.maps.Size(32, 32),
            // The origin for this image is (0, 0).
            origin: new google.maps.Point(0, 0),
            // The anchor for this image is the base of the flagpole at (0, 32).
            anchor: new google.maps.Point(16, 16)}
     return toreturn
} //makes an icon ready to the map

// QUERY to request for each node inside a region. With country code.
function clusterize(cluster) {

    var cian = iconMaker('cian.png')
    , red = iconMaker('red.png')
    , green = iconMaker('green.png')
    , yellow = iconMaker('yellow.png')
    , blue = iconMaker('blue.png')
    , magenta = iconMaker('magenta.png')

    var naranja = iconMaker('naranja.png')
    ,   violeta = iconMaker('violeta.png')
    ,   carmesi = iconMaker('carmesi.png')
    ,   verdeamarillo = iconMaker('verdeamarillo.png')
    ,   azulverde = iconMaker('azulverde.png')
    , ultramar = iconMaker('ultramar.png')
    ,   maxCluster = 0

    console.log(cluster)
    const keys = Object.keys(cluster)
    console.log(keys)
    for (i = 0; i < markers.length ; i++) {//return_dict[0].length; i++) {

        markers[i].cluster = 0
        markers[i].setIcon(null)
        markers[i].hide()

        console.log(markers[i].affid)
        var affid = markers[i].affid
        console.log(affid)
        console.log(cluster[affid])
        if (typeof cluster[affid] != 'undefined'){
            if (cluster[affid]['node_type'] != "Noise"){

            markers[i].cluster = cluster[affid]['cluster']
            if (markers[i].cluster > maxCluster) {maxCluster = markers[i].cluster};
            markers[i].show()

                    if (cluster[affid]['cluster'] == 1) {
                    markers[i].setIcon(cian)
                    } else if (cluster[affid]['cluster'] == 2) {
                    markers[i].setIcon(red)
                    } else if (cluster[affid]['cluster'] == 3) {
                    markers[i].setIcon(yellow)
                    } else if (cluster[affid]['cluster'] == 4) {
                    markers[i].setIcon(green)
                    } else if (cluster[affid]['cluster'] == 5) {
                    markers[i].setIcon(blue)
                    } else if (cluster[affid]['cluster'] == 6) {
                    markers[i].setIcon(magenta)
                    } else if (cluster[affid]['cluster'] == 7) {
                    markers[i].setIcon(ultramar)
                    } else if (cluster[affid]['cluster'] == 8) {
                    markers[i].setIcon(verdeamarillo)
                    } else if (cluster[affid]['cluster'] == 9) {
                    markers[i].setIcon(azulverde)
                    } else if (cluster[affid]['cluster'] == 10) {
                    markers[i].setIcon(violeta)
                    } else if (cluster[affid]['cluster'] == 11) {
                    markers[i].setIcon(carmesi)
                    } else if (cluster[affid]['cluster'] == 12) {
                    markers[i].setIcon(naranja)
                    }
                markers[i].node_type = cluster[affid]['node_type']

            }
        }
    }

    var clusterContent = `Ver cluster <input type="number" id="clusterNumber" name="eyes"
           placeholder="Select a Cluster" value='0'
           min="0" max='${maxCluster}' /> de ${maxCluster}`

    CLUSTER_TIMER_STOPPER = false
    document.getElementById('cluster_info').innerHTML = clusterContent
    document.getElementById("cluster_info").style.background = "initial";
    document.getElementById("cluster_info").style.fontSize = 'initial';

} // takes and object cluster dictionary and process it

function markerPrinter(id) {
    for (i = 0; i < markers.length ; i++) {//return_dict[0].length; i++) {
        if (markers[i].affid == id) {
            console.log(markers[i])
        }
        }




} //returns on console a maerker



function getPoints(){


    var heatmap_weight = document.getElementById('heatmap_weight');

    console.log(heatmap_weight)

    var toReturn = [];

     for (var i = 0; i < markers.length; i++) {

        if (arguments[0] == true){
            var checker = markers[i].cluster != 0
        } else {
            var checker = markers[i].active
        }

        if (checker) {

            //console.log(typeof locations[markers[i].affid]['lat'], locations[markers[i].affid]['lng'])

            var mylat = locations[markers[i].affid]['lat']
            , mylng = locations[markers[i].affid]['lng']
            , weight = markers[i].weight

            if (heatmap_weight.checked) {
                new_point = {location: new google.maps.LatLng(mylat, mylng), weight: weight}
                console.log('weighted: '+ new_point)
            } else {
                new_point = new google.maps.LatLng({lat: mylat , lng: mylng})
                console.log('no weight' + new_point)
            }


            new_point.affid = markers[i].affid
            //console.log(new_point)

            //console.log(new_point.lng())

            toReturn.push(new_point)

            //console.log(markers[i].affid)

        } else {console.log(markers[i].affid)}


    };
    console.log(toReturn)

    return toReturn
} // get active markers or cluster markers for the heatmap.


function infowindowContent(affil_dict,city,state,country,weight,cluster){


    var info = `<div id="contentInfoWindow" class="contentMap">
                <div class="contentImg" >
                    <img src="${affil_dict.logo_path}" title="${affil_dict.Name}" style="width:70px;"/>
                </div>
                <div class="contentTxt">
                <h2>${affil_dict.Name}</h2>
                    <p>
                        Situada en la ciudad de ${city}, ${state}, en el país de ${country}.
                        Aparece ${weight} veces en esta red, y hace parte del cluster ${cluster}


                    </p>
                </div>
                <div class="clear"></div>
            </div>`
    return info
}
