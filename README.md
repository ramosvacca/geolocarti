# gcarti
Geolocarti, versión en desarrollo de un GIS para la información sobre la producción científica en Colombia.

For Geolocarti to work we need to:

    - Set up Allegrograph (the repository) Server on port 10035
        - user: user
        - password: mio

    - Set up Python virtual environment with site-packages
        - agraph-python api
        - google.images.download
            - Change the version to save the files with the id of the affiliation

    - Set up socksv5h (the h makes resolve localhost on the proxy instead of our pc) proxy server on localhost:21331 to
      connect to the database on eiscapp.univalle.edu.co through a ssh tunnel. The only way to use agraph-python
      Api.
      ~ using the proxy with h at the end lets us resolve the localhost on the proxy server instead of local machine.
      ~ the only way to access SCOPUS files for full abstract or affiliation xml with API. And APIKEY

This application works as:

    - Open a connection = REPO_CONNECTION [CONNECTED THROUGH PROXY SERVER]
    - Takes a list of abstract IDs as the input.
      * LAUNCHES 30 THREADS
        - Checks each id on Scopus database.
            - If it is present, then downloads it and return the path of the file.
            - Else, it deletes the id from the list.
      * CLOSE THREADS
        - Returns a CLEAN_LIST, which only contains the abstract ids that are on SCOPUS

    - Inserts the files that are on CLEAN_LIST[0] to the repository [default name is 'pr1', given by
      the REPO_CONNECTION], the path file. CLEAN_LIST

    - Delete duplicate statements

    - Get the affiliations that are present on the graph under the abstract authors.
      * LAUNCHES 10 THREADS
        - It checks for each affiliation its existence in SCOPUS and returns a filepath if it is found,
          or deletes the id from the list if it is not present on SCOPUS.
      * CLOSES THREADS

      *LAUNCHES 30 THREADS
        - Makes an object for each ID
            - Gets each item on the list and takes its filepath to explore the XML, we search for the terms
              and insert them on the object.
                - With the terms we've gotten, we send the object to geocode it on google maps.
                    1st try on geocode API with full name and city, country, address.
                    2nd try on gocode api with name, city, country
                    3rd try from Google Maps SCREEN with name, city, country, address.
                    4th try from Google Maps SCREEN with name
                        - For the latter 2, we get the coords from google maps and then get the info
                          from geocoding them on Google Maps API.
            - Returns a full object for each ID that was on the list.
      * CLOSE THREADS

    - Inserts each property for each affiliation on the database as a triple [s, p, o]
        - It inserts an object with predicate 'glct:latlon_prueba_def' for each affiliation.
          The object is encoded on inserting to allegrograph with its own indexing format.
          - We can now make queries for the geographical space with lat and lon. !!!!!!!!!!!!!!!!!



