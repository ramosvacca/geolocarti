var start = 1996;
var end = new Date().getFullYear();
var options_start = "";
var options_end = "";

for(var year = start ; year <=end; year++){ //creates all the years for he years to start and end the query
    if (year != '1978') {
        options_start += "<option>"+ year +"</option>";
    }
     if( year != '2018') {
        options_end += "<option>"+ year +"</option>";
    }
    if (year == '1978'){
         options_start += "<option selected='selected'> 1978 </option>";
    }
    if (year == '2018'){
        options_end += "<option selected='selected'> 2018 </option>";
        options_start += "<option>"+ year +"</option>";
    }
}
document.getElementById("start_year").innerHTML = options_start ;
document.getElementById("final_year").innerHTML = options_end;

CLUSTER_TIMER_STOPPER = false

function clust_timer(){

    CLUSTER_TIMER_STOPPER = true
    var counter = 0
    ,   points = ''

    document.getElementById('cluster_info').innerHTML = 'Starting clusterization'
    document.getElementById("cluster_info").style.background = "orange";
    document.getElementById("cluster_info").style.fontSize = 'large';

    const timer_interval = setInterval(function () {

        if (CLUSTER_TIMER_STOPPER == true) { //It returns a list of affiliations ids
                if (counter == 0) {
            points = ''
            counter += 1

        } else if (counter == 1){
            points = '.'
            counter += 1

        } else if (counter == 2){
            points = '..'
            counter += 1

        } else if (counter == 3){
            points = '...'
            counter += 1

        } else if (counter == 4){
            points = '....'
            counter = 0

        }
                document.getElementById('cluster_info').innerHTML = `Clusterization in progress${points}`

        } else {
            clearInterval(timer_interval)
        }

    }, 700);


}

function listActive () {// List active nodes and send them to clusterize which on flask.
// then it takes the dictionary that comes with the clusters and send it as JSON to clusterize
//which then will send that after parsed to Draw
    clust_timer()

    toReturn = []

    for (var i = 0; i < markers.length; i++) {
        if (markers[i].active == true) {
            toReturn.push(markers[i].affid)
        } else {console.log(markers[i].affid)}
    };

    var cluster_local = undefined
    var minPts = document.getElementById("minPts").value
    , eps = document.getElementById("eps").value


    httpGetAsync(`http:/\/${base_HOST}:5000/dbscan_cluster?nodesList=[${toReturn}]&minPts=${minPts}&eps=${eps}`,
    function(response){console.log(response);
    cluster_local = response});

    const cluster_launch = setInterval(function () {

        if (typeof cluster_local != 'undefined') { //It returns a list of affiliations ids
        console.log(cluster_local)
        console.log(typeof cluster_local)
        var newobj = JSON.parse(cluster_local)
        console.log(newobj['60066812'])
        clusterize(newobj)
        clearInterval(cluster_launch)
    } else {console.log(typeof cluster_local)}
        }, 50);


} //Here we send the active nodes to clusterization



function httpGetAsync(theUrl, callback, additional){

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            if (typeof additional != 'undefined'){
                callback(xmlHttp.responseText, additional);
            } else {
                callback(xmlHttp.responseText);

            }
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous
    xmlHttp.send(null);

}

///////////////////// Actions ////////////////////////////////////////// Actions /////////////////////
///////////////////// Actions ////////////////////////////////////////// Actions /////////////////////
///////////////////// Actions ////////////////////////////////////////// Actions /////////////////////


document.getElementById('cluster_maker').onclick = function() {listActive()};


///////////////////// Actions ////////////////////////////////////////// Actions /////////////////////
///////////////////// Actions ////////////////////////////////////////// Actions /////////////////////
///////////////////// Actions ////////////////////////////////////////// Actions /////////////////////


function toggle_heatmap(){

    var toggler_state = document.getElementById('heatmap_toggler').innerHTML
    ,   color   = document.getElementById("heatmap_toggler").style.background

    console.log(toggler_state)

    if (document.getElementById("heatmap_toggler").style.background == "red"){

        document.getElementById("heatmap_toggler").style.background = "green";
        heatmap.setMap(mainmap)

    } else {

        document.getElementById("heatmap_toggler").style.background = "red";
        heatmap.setMap(null)

    }

}

function nodeTagger(){

    for (var i = 0; i < markers.length; i++) {


            var tosendQuery = tagQuery(markers[i].affid)
            ,   theUrl = baseUrl_query + encodeURIComponent(tosendQuery)

            function callbackFunc(answer, node){

                    var xmlDoc = $.parseXML( answer )
                    , $xml = $( xmlDoc ) //XML parsed
                    , results = $xml.find( "results" )
                    , single_results = results.find( "result" );

                    var city = single_results[0].getElementsByTagName("binding")[1].getElementsByTagName('literal')[0].innerHTML
                    , region = single_results[0].getElementsByTagName("binding")[2].getElementsByTagName('literal')[0].innerHTML
                    , country = single_results[0].getElementsByTagName("binding")[3].getElementsByTagName('literal')[0].innerHTML
                    , code =single_results[0].getElementsByTagName("binding")[4].getElementsByTagName('literal')[0].innerHTML

                    if (typeof single_results[1] != 'undefined') {
                        city = single_results[0].getElementsByTagName("binding")[1].getElementsByTagName('literal')[0].innerHTML

                    }

                    node.tag_loc = city
                    node.tag_reg = region
                    node.tag_country = country
                    node.tag_code = code

                    console.log(node, city)

                    //return [city, region, country, code]


                }

            httpGetAsync(theUrl, callbackFunc, markers[i])

    };
};

function relationsDiscovery(){

    var localId = document.getElementById("scopus_id_tofind").innerHTML;

    var local_loc = markers[markersDict[localId]].tag_loc
    ,   local_reg = markers[markersDict[localId]].tag_reg
    ,   local_country = markers[markersDict[localId]].tag_country
    ,   local_code = markers[markersDict[localId]].tag_code
    ,   locality_absolute = 0
    ,   region_absolute = 0
    ,   supra_absolute = 0
    ,   extra_absolute = 0
    ,   locality_weighted = 0
    ,   region_weighted = 0
    ,   supra_weighted = 0
    ,   extra_weighted = 0

    console.log(local_loc)



    if (arguments[0] == 0) {
        document.getElementById("table_tittle").innerHTML = 'Resultados del CLUSTER'
        activeNodes(0)

    } else if (typeof arguments[0] == 'number') {
        document.getElementById("table_tittle").innerHTML = 'Resultados del CLUSTER N° ' + arguments[0]
        activeNodes(arguments[0])

    }
    else {
        document.getElementById("table_tittle").innerHTML = 'Resultados de NODOS ACTIVOS'
    }


    for (var i = 0; i < markers.length; i++) {
        //console.log(typeof arguments[0])

        if (arguments[0] == 0) {
            var checker = markers[i].cluster != 0

        } else if (typeof arguments[0] == 'number') {
            var checker = arguments[0] == markers[i].cluster

        }
        else {
            var checker = markers[i].active
        }

        if (checker) {

            if (markers[i].tag_code == local_code) {
                supra_absolute += 1
                supra_weighted += markers[i].weight

                if (markers[i].tag_reg == local_reg){
                    region_absolute += 1
                    region_weighted += markers[i].weight

                    if (markers[i].tag_loc == local_loc){
                        locality_absolute += 1
                        locality_weighted += markers[i].weight

                    }

                }

            } else {
                extra_absolute += 1
                extra_weighted += markers[i].weight
            }

        }
    }


    var total_absolute = supra_absolute + extra_absolute
    ,   total_weighted = supra_weighted + extra_weighted


    document.getElementById("locality_absolute").innerHTML =  locality_absolute
    document.getElementById("locality_weighted").innerHTML =  locality_weighted

    document.getElementById("region_absolute").innerHTML = region_absolute-locality_absolute
    document.getElementById("region_weighted").innerHTML = region_weighted-locality_weighted

    document.getElementById("supra_absolute").innerHTML = supra_absolute-region_absolute
    document.getElementById("supra_weighted").innerHTML = supra_weighted-region_weighted

    document.getElementById("extra_absolute").innerHTML = extra_absolute
    document.getElementById("extra_weighted").innerHTML = extra_weighted

    document.getElementById("total_absolute").innerHTML = total_absolute
    document.getElementById("total_weighted").innerHTML = total_weighted
    document.getElementById("total_average").innerHTML = (total_weighted / total_absolute).toFixed(2)

    document.getElementById("locality_average").innerHTML =  (locality_weighted / locality_absolute).toFixed(2)
    document.getElementById("locality_absolutePercentage").innerHTML =  (locality_absolute / total_absolute * 100).toFixed(2)
    document.getElementById("locality_weightedPercentage").innerHTML =  (locality_weighted / total_weighted * 100).toFixed(2)

    document.getElementById("region_average").innerHTML =  ((region_weighted-locality_weighted)/(region_absolute - locality_absolute)).toFixed(2)
    document.getElementById("region_absolutePercentage").innerHTML =  ((region_absolute - locality_absolute)/ total_absolute * 100).toFixed(2)
    document.getElementById("region_weightedPercentage").innerHTML =  ((region_weighted-locality_weighted)/ total_weighted * 100).toFixed(2)

    document.getElementById("supra_average").innerHTML =  ((supra_weighted-region_weighted) /(supra_absolute-region_absolute)).toFixed(2)
    document.getElementById("supra_absolutePercentage").innerHTML =  ((supra_absolute-region_absolute) / total_absolute * 100).toFixed(2)
    document.getElementById("supra_weightedPercentage").innerHTML =  ((supra_weighted-region_weighted) / total_weighted * 100).toFixed(2)

    document.getElementById("extra_average").innerHTML =  (extra_weighted /extra_absolute).toFixed(2)
    document.getElementById("extra_absolutePercentage").innerHTML =  (extra_absolute / total_absolute * 100).toFixed(2)
    document.getElementById("extra_weightedPercentage").innerHTML =  (extra_weighted / total_weighted * 100).toFixed(2)


} /*Discover the type of relation for each marker that was active, or that was in cluster.
and adds it to the correct relation type on the table. also changes the table tittle.*/


function activenodesHeatmap(){

    heatmap.setData(getPoints(arguments[0]))

    if (arguments[0] == true) {
    document.getElementById('heatmap_toggler').innerHTML = 'clusterNodes'
    document.getElementById("heatmap_toggler").style.background = "green";

    } else {
    document.getElementById('heatmap_toggler').innerHTML = 'activeNodes'
    document.getElementById("heatmap_toggler").style.background = "green";
    }

} // a function that uses getPoints to get the markers to show on the heatmap and sets them
//on the heatmap data place