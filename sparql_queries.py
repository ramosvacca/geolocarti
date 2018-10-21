num_univs = """# View triples
PREFIX glct: <http://www.gcarti.co/mc/geodata/>
select ?affnom ?affid 	(count(?affnom) as ?num_univs){

  SELECT distinct ?abtract_id_res ?affnom ?affid
                     {
                       
  	?abtract_id_res dc:creator [?seq_item ?author_about ].
  
	?author_about ?affiliation ?aff_res .
                       
  	?aff_res skos:prefLabel ?affnom .
  	?aff_res elsapi:afid ?affid .
                       
  #MINUS {?aff_res glct:latlon_prueba_def ?coordenadas}               
  } 
					
} group by ?affnom ?affid order by desc(?num_univs)"""

allInfo_query = """PREFIX glct: <http://www.gcarti.co/mc/geodata/>
select ?affnom ?affid ?lat ?lng ?city ?country ?aal_1 (count(?affid) as ?num_univs) {

  SELECT distinct ?abtract_id_res ?affnom ?affid ?lat ?lng ?city ?country ?aal_1
                     { 
  ?abtract_id_res dc:creator ?author_seq . 
  ?author_seq ?seq_item ?author_about .
  ?author_about ?affiliation ?aff_res .
  ?aff_res skos:prefLabel ?affnom .
  ?aff_res elsapi:afid ?affid .
  ?aff_res glct:lat ?lat .
  ?aff_res glct:lng ?lng .
  ?aff_res glct:city ?city .
  ?aff_res glct:country ?country .
  ?aff_res glct:aal_1 ?aal_1 .
                       
                     } #order by asc(?affnom)
					} group by ?affnom ?affid ?lat ?lng ?city ?country ?aal_1 order by desc(?num_univs)
"""

in_circle = """

SELECT DISTINCT ?affil ?afid ?lat ?lon ?nom{

{?affil nd:inCircle (glct:latlon_prueba_def :lat 3.3 :lon -73.7

                                          :radius 10 :units :km) .
  }
  ?affil elsapi:afid ?afid .
  ?affil glct:lat ?lat .
  ?affil glct:lng ?lon . 
  ?affil skos:prefLabel ?nom.
  }
  
  """
links_query = """PREFIX glct: <http://www.gcarti.co/mc/geodata/>
SELECT ?abstract_id_res ?affnom ?affid
                     { 
  ?abstract_id_res dc:creator ?author_seq . 
  ?author_seq ?seq_item ?author_about .
  ?author_about ?affiliation ?aff_res .
  ?aff_res skos:prefLabel ?affnom .
  ?aff_res elsapi:afid ?affid .
                   }"""