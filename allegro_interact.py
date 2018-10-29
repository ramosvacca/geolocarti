from threading import Thread
from franz.openrdf.query.query import QueryLanguage
from franz.openrdf.repository.attributes import AttributeDefinition
from franz.openrdf.rio.rdfformat import RDFFormat
import re
import sparql_queries
import math
from personal import setenvar
from google_images_download import geolocarti_images_download   #importing the library
import os



def aff_count_query(repo_conn_object, query_str=sparql_queries.num_univs):  # query to get the affiliations and the number of times it is counted

    tuple_query = repo_conn_object.prepareTupleQuery(QueryLanguage.SPARQL, query_str)  # preparar la consulta con la API
    result = tuple_query.evaluate()  # meter los resultados en variable

    affs = []  # arreglo para guardar cada afiliacion, su nombre y las apariciones en listas

    with result:
        for binding_set in result:
            s = binding_set.getValue("affnom")
            p = binding_set.getValue("affid")
            o = re.search("\d+", str(binding_set.getValue("num_univs"))).group()
            affs = affs + [[s, p, o]]  # se agrega cada lista al arreglo affs
            # print("%s %s %s" % (s, p, o))
    return(affs)

def allInfo_query(conn_object, query_str=sparql_queries.allInfo_query,th_launch=15, approved_nodes=[]):

    """
    We need to extract the main information concerning the


    :param conn_object:
    :param query_str:
    :return:
    """

    tuple_query = conn_object.prepareTupleQuery(QueryLanguage.SPARQL,
                                                     query_str)  # preparar la consulta con la API
    result = tuple_query.evaluate()  # meter los resultados en variable

    affs = []  # arreglo para guardar cada afiliacion, su nombre y las apariciones en listas
    locations = {}


    with result:

        for binding_set in result:
            print(binding_set)
            name = binding_set.getValue("affnom")
            scopus_id = binding_set.getValue("affid")
            count = int(re.search("\d+", str(binding_set.getValue("num_univs"))).group())
            lat = binding_set.getValue("lat")
            lng = binding_set.getValue("lng")
            city = binding_set.getValue("city")
            country = binding_set.getValue("country")
            aal_1 = binding_set.getValue("aal_1")
            zoom = 8

            radio = 0

            if count <= 30:
                radio = count * 8
            elif count <= 50:
                radio = count * 7
            elif count <= 80:
                radio = count * 6
            elif count <= 150:
                radio = count * 5
            elif count <= 200 :
                radio = count * 4
            elif count <= 400:
                radio = count * 3
            else:
                radio = count * 2
            radio = radio * 10


            print(float(str(lat).replace('"',"")))


            affs.append({'Name':name,
                         'Content':'Aparece ' + str(count)+ ' veces.'+ '\nState: '+str(aal_1),
                         'Radio':radio,
                         'Zoom': zoom,
                         'count':count,
                         'affid':cleaner(scopus_id),
                         'city':city,
                         'country':country,
                         'final_id':'affid-'+cleaner(scopus_id),
                         'region':aal_1
                         }) # se agrega cada lista al arreglo affs
            # print("%s %s %s" % (s, p, o))

            locations[cleaner(scopus_id)]={"lat":float(str(lat).replace('"',"")),
                         "lng":float(str(lng).replace('"',""))}
            approved_nodes.append(cleaner(scopus_id))

    print('affs in a interact ' + str(affs))
    setenvar(proxy=False) # We need to deactivate the proxy as google_images_download will use them through urllib


    #Prepare to launche th_launch threads to download logos and get paths
    chunksize = int(math.ceil(len(affs) / float(th_launch)))

    threads = []


    for i in range(th_launch):
        t = Thread(
            target=pathMaker_segment,
            args=(affs, (chunksize * i), (chunksize * (i + 1)))
        )

        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    setenvar(proxy=False)#100782160

    bubble_sort(affs)

    add_zIndex(affs)

    print(locations)
    path = 'visual_interface/locations_latlng.txt'
    places_locations = open(path, 'w')
    places_locations.write(str(locations))

    return (affs)

def add_zIndex(dict_list):
    count = 0

    for aff_dict in dict_list:
        aff_dict['z-index']=5000+count
        count+=1

def bubble_sort(collection):
    length = len(collection)
    for i in range(length):
        for j in range(length - 1):

            if collection[j]['count'] < collection[j + 1]['count']:

                collection[j], collection[j + 1] = collection[j + 1], collection[j]

def cleaner(word_toClean, type=str):

    if type == str:
        return (str(word_toClean).replace(',', "").replace("-",''))

def downloadImage_PathReturn(affid_tofind, keyword):

    arguments = {"keywords": keyword, "limit": 1, 'image_directory': 'all', 'affid': affid_tofind}

    print(arguments)

    paths = geolocarti_images_download.googleimagesdownload().download(
        arguments)  # passing the arguments to the function

    return (paths[keyword][0])

      # printi# ng absolute paths of the downloaded images

def pathMaker_segment(list, start, end, prefix='../../', dir='downloads/all/',):

    for aff_no in range(start, end):
        file_exists = False

        for file in os.listdir(dir):

            if file.startswith(cleaner(list[aff_no]['affid'])):
                print(os.path.join(prefix, dir, file))
                list[aff_no]['logo_path'] = (os.path.join(prefix, dir, file))
                file_exists = True
        if not file_exists:
            try:
                list[aff_no]['logo_path'] = downloadImage_PathReturn(
                    affid_tofind=cleaner(list[aff_no]['affid']),
                    keyword=cleaner(list[aff_no]['Name'])+' logo'
                )
            except:
                try:
                    list[aff_no]['logo_path'] = downloadImage_PathReturn(
                    affid_tofind=cleaner(list[aff_no]['affid']),
                    keyword=cleaner(list[aff_no]['Name']) + cleaner(list[aff_no]['city']) + ' logo'
                    )
                except:
                    try:
                        list[aff_no]['logo_path'] = downloadImage_PathReturn(
                            affid_tofind=cleaner(list[aff_no]['affid']),
                            keyword=cleaner(list[aff_no]['Name'])
                            )
                    except:
                        list[aff_no]['logo_path'] = '../../downloads/nologo.png'

def links_weighted(repo_conn_object, query_str=sparql_queries.links_query, approved_nodes=[]):  # query to get the affiliations and the number of times it is counted
    print("Generating the main weighted network")
    print(approved_nodes)
    tuple_query = repo_conn_object.prepareTupleQuery(QueryLanguage.SPARQL, query_str)  # preparar la consulta con la API
    result = tuple_query.evaluate()  # meter los resultados en variable

    links = []  # diccionario que contiene los enlaces y sus pesos

    with result:
        for binding_set in result:

            p = binding_set.getValue("affid")
            o = binding_set.getValue("abstract_id_res")

            if cleaner(p) in approved_nodes:
                links = links + [[o, p]]

    separated_links = {} #dic with {-i-abs_id: -in_dict[i]-[and a list of -aff-[aff_ids]],} that appear on it


    for pair in links:
        abs_id = str(pair[0])

        if abs_id in separated_links:
            separated_links[abs_id] += [pair[1]]
            separated_links[abs_id].sort()
        else:
            new_list = [pair[1]]
            separated_links[abs_id] = new_list

    print(separated_links)

    return(network_maker(separated_links))

def network_maker(in_dict):

    weighted_links={}
    list_ids = []

    for i in in_dict.keys():  # each list

        for aff in range(len(in_dict[i])):

            for couple in range(len(in_dict[i])-1):

                if aff+couple+1 <= len(in_dict[i])-1:
                    node_1 = in_dict[i][aff]
                    node_2 = in_dict[i][aff+couple+1]

                    nodename = cleaner(node_1) + '_' + cleaner(node_2)

                    if nodename in weighted_links:
                        weighted_links[nodename]['weight'] += 1

                    else:
                        newnode = {'node1':cleaner(node_1), 'node2':cleaner(node_2), 'weight': 1}

                        weighted_links[nodename] = newnode

                        list_ids += [nodename]
    print(list_ids)
    return weighted_links

def weighted_links_inserter(weighted_links, repo_conn):

    weight = AttributeDefinition(name='weight')
    repo_conn.setAttributeDefinition(weight)
    repo_conn.commit()


    link_nQuad = '<https://api.elsevier.com/content/affiliation/affiliation_id/%s> <http://www.gcarti.co/mc/geodata/link> <https://api.elsevier.com/content/affiliation/affiliation_id/%s> {"weight": "%d"} .'


    for i in weighted_links.keys():
        link_triple = link_nQuad % ((weighted_links[i]['node1'], weighted_links[i]['node2'], weighted_links[i]['weight']))
        #print(link_triple)
        repo_conn.addData(link_triple, rdf_format=RDFFormat.NQX)