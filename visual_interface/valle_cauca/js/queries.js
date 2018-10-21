PREFIX attr: <http://franz.com/ns/allegrograph/6.2.0/>
PREFIX glct: <http://www.gcarti.co/mc/geodata/>
PREFIX tags: <http://www.gcarti.co/mc/tags/>

   SELECT ?o ?a ?foundCity

{ BIND(<https://api.elsevier.com/content/affiliation/affiliation_id/60013528> as ?affid)


 {?affid tags:city ?foundCity}
	BIND(?foundCity as ?city)
 {
       	?affid 	glct:link ?o ;
       	 		skos:prefLabel ?name.

		?o skos:prefLabel ?name_ ;
           tags:city ?city .

      	?a attr:attributes (?affid glct:link ?o) .
   	} UNION
	{
   		?o 	glct:link ?affid;
      		skos:prefLabel ?name_;
            tags:city ?city .

    	?affid skos:prefLabel ?name .


    	?a attr:attributes (?o glct:link ?affid ) .
	}

}

ORDER BY ?a
