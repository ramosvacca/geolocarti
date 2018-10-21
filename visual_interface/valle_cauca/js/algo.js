var prefixes = 'PREFIX glct: <http://www.gcarti.co/mc/geodata/> PREFIX tags: <http://www.gcarti.co/mc/tags/> PREFIX elsapi:<http://www.elsevier.com/xml/svapi/rdf/dtd/> PREFIX prism:<http://prismstandard.org/namespaces/basic/2.0/>';


//citations, coauthorship, references

function sparqlQuery (affid, outer_region, queryType, subRegion, ...resto)  {

    var look_for = document.getElementById('lookfor').value;
    var type_definer = ''
    , author_restricted = ''

    //Author restricted ES OPCIONAL
 	if (author_restricted != '') {author_restricted = `
 	BIND (<https:/\/api.elsevier.com/content/author/author_id/${author_id}> as ?authors_id)`
 	}

    if(look_for == 'coauthorship'){ //coauthorship
  	    local_abstract = '?abstract_id'
        ref_abstract = '?abstract_id'
    } else if (look_for == 'references'){ //reference
 	local_abstract = '?abstract_id'
    ref_abstract = '?ref_abstract_id'
 	type_definer = '?abstract_id elsapi:reference ?ref_abstract_id .'
    } else if (look_for == 'citations'){ //citations
   	local_abstract = '?ref_abstract_id'
    ref_abstract = '?abstract_id'
 	type_definer = '?abstract_id elsapi:reference ?ref_abstract_id .'
    } else if (look_for == 'not_linked') {

     local_abstract = '?abstract_id'
     ref_abstract = '?ref_abstract_id'
     type_definer = ` MINUS{?ref_affid glct:link  ?localID}
           MINUS {?localID glct:link ?ref_affid} .
        `

     }
    console.log('restooooo'+resto[0].nodeCountry)

    if (resto[0].nodeCountry == undefined) { //Defining when requesting the network of a node and a COUNTRY
        if (queryType == 'allinRegion') { //in region
  	        region_restriction = `?ref_affid tags:${outer_region} ?myRegion`
        } else if (queryType == 'outofRegion') { //off region
  	        region_restriction = `FILTER NOT EXISTS {?ref_affid tags:${outer_region} ?myRegion }`
        } else if (queryType == 'inRegion_offSubregion') { //in region - off subRegion
    region_restriction = `?localID  tags:${subRegion} ?mysubRegion .
  	FILTER NOT EXISTS {?ref_affid tags:${subRegion} ?mysubRegion }
	FILTER EXISTS {?ref_affid tags:${outer_region} ?myRegion }`
    } else if (queryType == 'offRegion_inSubregion') { //off region - in subRegion
	region_restriction = `?localID tags:${subRegion} ?mysubRegion .
   	FILTER NOT EXISTS {?ref_affid tags:${outer_region} ?myRegion . ?ref_affid tags:${subRegion} ?othersubRegion .
          FILTER (?othersubRegion != ?mysubRegion)}`
    }
    } else {

    region_restriction = `?ref_affid tags:code \"${resto[0].code}\"`

    }

    ///////////QUERY STARTS QUERY STARTS // QUERY STARTS QUERY STARTS // QUERY STARTS QUERY STARTS /////////////
    //HEADER QUERY  -------- HEADER QUERY ###
    queryBase = `SELECT ?ref_affid (count (?ref_affid) as ?counted) {
    SELECT DISTINCT ?ref_affid ${ref_abstract}
    {	BIND(<https:/\/api.elsevier.com/content/affiliation/affiliation_id/${affid}> as ?localID)

 	${author_restricted}

 	?authors_id elsapi:affiliation  ?localID .
  	?ref_authors_id elsapi:affiliation ?ref_affid.
  	?abstract_id prism:copyrightYear ?abstract_id_year .
 		${local_abstract}	dc:creator [?number_in_cluster ?authors_id ] .
 		${ref_abstract} 	dc:creator [?ref_number_in_cluster ?ref_authors_id ].
 		${type_definer}

 		${local_abstract} ?authors_id ?localID .
        ${ref_abstract} ?ref_authors_id ?ref_affid .

 	?localID tags:${outer_region} ?myRegion .
 	${region_restriction}

  	FILTER (?ref_authors_id != ?authors_id) FILTER (?number_in_cluster != ?ref_number_in_cluster) FILTER (?ref_affid != ?localID)
	 FILTER (?abstract_id_year >= \"${resto[0].start_year}\") FILTER (?abstract_id_year <= \"${resto[0].final_year}\")

    } } group by  ?ref_affid`

    return prefixes + queryBase

};

 //CIRCLEQUERY ///// CIRCLE QUERY CIRCLE QUERY CIR

function sparql_circleQuery(affid, queryType, lat, lon, circle1_radius, circle2_radius){
 console.log(affid, circle2_radius)
    var look_for = document.getElementById('lookfor').value;
    var before_closing = ''
        , after_circleQuery = ''
        , before_opening = ''
        , after_closing = '';
        var local_not = ''


 var circles_referenceQuery = `SELECT DISTINCT ?ref_affid
    {BIND(<https:/\/api.elsevier.com/content/affiliation/affiliation_id/${affid}> as ?localID)

?abstract_id <http:/\/www.elsevier.com/xml/svapi/rdf/dtd/reference> ?ref_abstract_id .
  ?ref_abstract_id <http:/\/purl.org/dc/elements/1.1/creator> ?cluster_ref .
  ?cluster_ref ?number_in_cluster_ref ?authors_id_ref .
  ?authors_id_ref <http:/\/www.elsevier.com/xml/svapi/rdf/dtd/affiliation>  ?ref_affid .

  ?abstract_id <http:/\/purl.org/dc/elements/1.1/creator> ?cluster .
  ?cluster ?number_in_cluster ?authors_id .
  ?authors_id <http:/\/www.elsevier.com/xml/svapi/rdf/dtd/affiliation>  ?localID .

	FILTER (?abstract_id != ?ref_abstract_id) FILTER (?ref_affid != ?localID )

  `
  var circles_citationsQuery = `prefix glct:<http:/\/www.gcarti.co/mc/geodata/>
    SELECT DISTINCT ?citingID

  {BIND(<https:/\/api.elsevier.com/content/affiliation/affiliation_id/${affid}> as ?localID)


 	?authors_id <http:/\/www.elsevier.com/xml/svapi/rdf/dtd/affiliation> ?localID .
 	?cluster ?number_inCluster ?authors_id .
 	?abstract_id <http:/\/purl.org/dc/elements/1.1/creator> ?cluster .


	?citing_authors_id <http:/\/www.elsevier.com/xml/svapi/rdf/dtd/affiliation> ?citingID .
 	?citing_cluster ?numberciting_inCluster ?citing_authors_id .
 	?citing_abstract_id <http:/\/purl.org/dc/elements/1.1/creator> ?citing_cluster .
 	?citing_abstract_id <http:/\/www.elsevier.com/xml/svapi/rdf/dtd/reference> ?abstract_id .
   `
//END OF QUERY BASE




    if (queryType == 'inCircle1'){

        if(look_for == 'references'){

        var filter = `FILTER EXISTS {?ref_affid nd:inCircle (glct:latlon_prueba_def keyword:lat ${lat} keyword:lon ${lon} keyword:radius ${circle1_radius} keyword:units keyword:km) .} }`


        return prefixes + circles_referenceQuery +filter

        }
        else if (look_for == 'citations') {

            var filter = `FILTER EXISTS {?citingID nd:inCircle (glct:latlon_prueba_def keyword:lat ${lat} keyword:lon ${lon} keyword:radius ${circle1_radius} keyword:units keyword:km) .} }`

            return prefixes + circles_citationsQuery + filter
        }


        query_suffix = ''

    };
    


    if (queryType == 'offCircle1'){
        
        if (look_for == 'references') {
            var filter = `FILTER NOT EXISTS {?ref_affid nd:inCircle (glct:latlon_prueba_def keyword:lat ${lat} keyword:lon ${lon} keyword:radius ${circle1_radius} keyword:units keyword:km) .} }`

            return prefixes + circles_referenceQuery + filter

        } else if (look_for == 'citations') {

            var filter = `FILTER NOT EXISTS {?citingID nd:inCircle (glct:latlon_prueba_def keyword:lat ${lat} keyword:lon ${lon} keyword:radius ${circle1_radius} keyword:units keyword:km) .} }`

            return prefixes + circles_citationsQuery + filter
        }
        console.log(circle2_radius)
        before_opening = '?affil elsapi:afid ?afid . MINUS '

    }
    if (queryType == 'offCircle1_onCircle2'){

        if (look_for == 'references') {
        var filter = `FILTER EXISTS {?ref_affid nd:inCircle (glct:latlon_prueba_def keyword:lat ${lat} keyword:lon ${lon}

                                          keyword:radius ${circle2_radius} keyword:units keyword:km) .}

  FILTER NOT EXISTS {?ref_affid nd:inCircle (glct:latlon_prueba_def keyword:lat ${lat} keyword:lon ${lon}

                                          keyword:radius ${circle1_radius} keyword:units keyword:km) .}}`
        return prefixes + circles_referenceQuery + filter
        } else
        if (look_for == 'citations') {
            filter = `FILTER EXISTS {?ref_affid nd:inCircle (glct:latlon_prueba_def keyword:lat ${lat} keyword:lon ${lon}

                                          keyword:radius ${circle2_radius} keyword:units keyword:km) .}

  FILTER NOT EXISTS {?ref_affid nd:inCircle (glct:latlon_prueba_def keyword:lat ${lat} keyword:lon ${lon}

                                          keyword:radius ${circle1_radius} keyword:units keyword:km) .}}`
        return prefixes + circles_citationsQuery + filter
        }

        console.log('debuggin, inserting 2 radius ' + circle2_radius)
        before_opening = `{
            ?affil nd:inCircle (glct:latlon_prueba_def keyword:lat ${lat} keyword:lon ${lon}

                                          keyword:radius ${circle2_radius} keyword:units keyword:km) .
                }
            MINUS`

    }
    if (queryType == 'onCircle1_offCircle2'){
        if (look_for == 'references') {
        var fullQuery = `SELECT DISTINCT ?ref_affid
{
  {
  BIND(<https:/\/api.elsevier.com/content/affiliation/affiliation_id/${affid}> as ?myaffid)

?abstract_id <http:/\/www.elsevier.com/xml/svapi/rdf/dtd/reference> ?ref_abstract_id .
  ?ref_abstract_id <http:/\/purl.org/dc/elements/1.1/creator> ?cluster_ref .
  ?cluster_ref ?number_in_cluster_ref ?authors_id_ref .
  ?authors_id_ref <http:/\/www.elsevier.com/xml/svapi/rdf/dtd/affiliation>  ?ref_affid .

  ?abstract_id <http:/\/purl.org/dc/elements/1.1/creator> ?cluster .
  ?cluster ?number_in_cluster ?authors_id .
  ?authors_id <http:/\/www.elsevier.com/xml/svapi/rdf/dtd/affiliation>  ?localID .

	FILTER (?abstract_id != ?ref_abstract_id) FILTER (?ref_affid != ?localID ) 
 FILTER EXISTS {?ref_affid nd:inCircle (glct:latlon_prueba_def keyword:lat ${lat} keyword:lon ${lon}

                                          keyword:radius ${circle1_radius} keyword:units keyword:km) .}

  } UNION {
  BIND(<https:/\/api.elsevier.com/content/affiliation/affiliation_id/${affid}> as ?myaffid)

?abstract_id <http:/\/www.elsevier.com/xml/svapi/rdf/dtd/reference> ?ref_abstract_id .
  ?ref_abstract_id <http:/\/purl.org/dc/elements/1.1/creator> ?cluster_ref .
  ?cluster_ref ?number_in_cluster_ref ?authors_id_ref .
  ?authors_id_ref <http:/\/www.elsevier.com/xml/svapi/rdf/dtd/affiliation>  ?ref_affid .

  ?abstract_id <http:/\/purl.org/dc/elements/1.1/creator> ?cluster .
  ?cluster ?number_in_cluster ?authors_id .
  ?authors_id <http:/\/www.elsevier.com/xml/svapi/rdf/dtd/affiliation>  ?localID .

	FILTER (?abstract_id != ?ref_abstract_id) FILTER (?ref_affid != ?localID ) 
 FILTER NOT EXISTS {?ref_affid nd:inCircle (glct:latlon_prueba_def keyword:lat ${lat} keyword:lon ${lon}

                                          keyword:radius ${circle2_radius} keyword:units keyword:km) .}

  }}`

    return prefixes + fullQuery


        }

        if (look_for == 'citations') {
        localQuery = `
SELECT DISTINCT ?ref_affid
{
  {
  BIND(<https:/\/api.elsevier.com/content/affiliation/affiliation_id/${affid}> as ?myaffid)

?ref_abstract_id <http:/\/www.elsevier.com/xml/svapi/rdf/dtd/reference> ?abstract_id .
  ?ref_abstract_id <http:/\/purl.org/dc/elements/1.1/creator> ?cluster_ref .
  ?cluster_ref ?number_in_cluster_ref ?authors_id_ref .
  ?authors_id_ref <http:/\/www.elsevier.com/xml/svapi/rdf/dtd/affiliation>  ?ref_affid .

  ?abstract_id <http:/\/purl.org/dc/elements/1.1/creator> ?cluster .
  ?cluster ?number_in_cluster ?authors_id .
  ?authors_id <http:/\/www.elsevier.com/xml/svapi/rdf/dtd/affiliation>  ?localID .

	FILTER (?abstract_id != ?ref_abstract_id) FILTER (?ref_affid != ?localID ) 
 FILTER EXISTS {?ref_affid nd:inCircle (glct:latlon_prueba_def keyword:lat ${lat} keyword:lon ${lon}

                                          keyword:radius ${circle1_radius} keyword:units keyword:km) .}

  } UNION {
  BIND(<https:/\/api.elsevier.com/content/affiliation/affiliation_id/${affid}> as ?myaffid)

?ref_abstract_id <http:/\/www.elsevier.com/xml/svapi/rdf/dtd/reference> ?abstract_id .
  ?ref_abstract_id <http:/\/purl.org/dc/elements/1.1/creator> ?cluster_ref .
  ?cluster_ref ?number_in_cluster_ref ?authors_id_ref .
  ?authors_id_ref <http:/\/www.elsevier.com/xml/svapi/rdf/dtd/affiliation>  ?ref_affid .

  ?abstract_id <http:/\/purl.org/dc/elements/1.1/creator> ?cluster .
  ?cluster ?number_in_cluster ?authors_id .
  ?authors_id <http:/\/www.elsevier.com/xml/svapi/rdf/dtd/affiliation>  ?localID .

	FILTER (?abstract_id != ?ref_abstract_id) FILTER (?ref_affid != ?localID ) 
 FILTER NOT EXISTS {?ref_affid nd:inCircle (glct:latlon_prueba_def keyword:lat ${lat} keyword:lon ${lon}

                                          keyword:radius ${circle2_radius} keyword:units keyword:km) .}

  }}`
        return prefixes + localQuery
        }


        before_opening = `{?affil elsapi:afid ?id_number
 MINUS
         {
?affil nd:inCircle (glct:latlon_prueba_def keyword:lat ${lat} keyword:lon ${lon}

                                          keyword:radius ${circle2_radius} keyword:units keyword:km) .
 }}
UNION`

    }

    if (links=='Linked'){
        after_closing = 'FILTER EXISTS {{OPTIONAL {?affil glct:link ?myaffid}}UNION {OPTIONAL {?myaffid glct:link ?affil} }}'
        };
    if (links == 'NotLinked'){
        after_closing = 'FILTER NOT EXISTS {{OPTIONAL {?affil glct:link ?myaffid}}UNION {OPTIONAL {?myaffid glct:link ?affil} }}'
    };

     var localQuery = `
SELECT DISTINCT ?affil
{BIND(<https:/\/api.elsevier.com/content/affiliation/affiliation_id/${affid}> as ?myaffid)
${before_opening}
{
?affil nd:inCircle (glct:latlon_prueba_def keyword:lat ${lat} keyword:lon ${lon}

                                          keyword:radius ${circle1_radius} keyword:units keyword:km) .
    ${after_circleQuery} ${before_closing} } ${after_closing}
  }`

    var myQuery = prefixes + localQuery
    console.log(affid + 'on query')
    //It returns a list of affiliations ids
    return myQuery
 }


 /////// SYSTEM QUERIES


function countrynodesQuery (country_code) {

    localQuery = `SELECT DISTINCT ?affid WHERE {

	?affid tags:code \"${country_code}\" .

}`

return prefixes + localQuery


}



function tagQuery (affid){
    var localQuery = `# View triples
SELECT DISTINCT ?myId ?city ?region ?country ?code {
  BIND (<https:/\/api.elsevier.com/content/affiliation/affiliation_id/${affid}> as ?myId)
   ?myId ?p ?o;
	tags:city ?city; tags:state ?region; tags:country ?country; tags:code ?code.
}`

return prefixes + localQuery

}