import requests
import xml.etree.ElementTree as ET
import os
import tech
import math
from threading import Thread
import time


def elsevier_interact(socpus_id, req_type, checkonly=False):  # to download an affiliation xml file
    """
    Downloads the requested id from ELSEVIER API if the file is not present on local directory
    and returns
    the filepath.
        If response 401 you are trying to access ELSEVIER API from an unauthorized IP and quits.
        If response is 404, the file was not found and continues without downloading it. We should
        not see this.
        For any other response, the program quits and shows the original response from ELSEVIER API.
    :return:
    :param socpus_id:
    :param req_type: can be 'affil' for affiliation [affiliation retrieval]
        or 'abstr' for abstracts and articles [abstract retrieval].
    :param checkonly: If True, the function returns 1 when the resource is found and 0 when is not found
        on ELSEVIERs API.
    :return: When checkonly param is set to TRUE, returns 1 when resource found, otherwise returns 0.
            When checkonly param is FALSE, returns filepath.
    """

    elsevier_apikey = os.environ.get('ELSEVIER_APIKEY')
    base_url = 'https://api.elsevier.com/content/'
    if req_type == 'affil':
        url_suf = 'affiliation/affiliation_id/'
        req_Accept = 'xml'
        d_folder = 'xmls/'
        f_type = '.xml'
    elif req_type == 'abstr':
        url_suf = 'abstract/scopus_id/'
        req_Accept = 'rdf+xml'
        d_folder = 'abstract_rdf/'
        f_type = '.rdf'

    print(base_url + url_suf + socpus_id)

    try:
        open(d_folder + socpus_id + f_type, 'r')
        filepath = d_folder + socpus_id + f_type

        if checkonly:
            mk_msg = socpus_id + ', is using an stored file found on ' + d_folder + '. You can delete it to check it again from Scopus servers.'
            tech.report_log(mk_msg, 'stored_resources')

            return True

        return filepath

    except FileNotFoundError:

        elsevapi_response = requests.get(base_url + url_suf + socpus_id,
                                         headers={'Accept': 'application/' + req_Accept,
                                                  'X-ELS-APIKey': elsevier_apikey}
                                         )

        if str(elsevapi_response) == '<Response [200]>':

            print(f_type + ' file ok from Elsevier API. Authorized IP.')

            tosave = elsevapi_response.text.encode('utf-8')  # make tree from

            f = open(d_folder + socpus_id + f_type, "w+")
            f.write(str(tosave.decode('utf-8', 'ignore')))

            if checkonly:
                mk_msg = socpus_id + ' ' + req_type + ' ' + f_type + ' file downloaded to ' + d_folder + 'while checking. '
                tech.report_log(mk_msg, 'stored_resources')
                return True

            filepath = d_folder + socpus_id + f_type

            return filepath

        elif str(elsevapi_response) == '<Response [401]>':
            print('Unauthorized access for Elsevier API. Connecting from an unknown IP.')
            """
            Si el acceso a la API de Elsevier no es autorizado, the most probable cause is that the IP
            from where you are requesting the information is not the authorized one for the APIkey. Elsevier
            APIkeys only work under the IP for which were obtained. ELSEVIER API does not work from not authorized IP
            Addresses
            """
            quit()

        elif str(elsevapi_response) == '<Response [404]>':

            if checkonly:
                return False
                print(elsevapi_response)

            print('Elsevier API did not found a resource for ' + socpus_id)


        else:
            print(socpus_id + ' revisar error')
            print(elsevapi_response)
            quit()

###############################################################################

def threaded_checker(list_tocheck, req_type, th_launch):
    """
    Takes a list of Scopus IDs to check whether they are in the repository. Can be affiliation
    """
    final_list = []

    def auxiliar(matrix, final_list, contando):

        for item in matrix:
            if elsevier_interact(item, req_type, True) == True:
                final_list.append(item)
            else:
                errormessage = req_type + ' id: ' + item + ' was not found in SCOPUS by ID item. Removed from original list\n'
                tech.report_log(errormessage, 'errorlog')

    chunksize = int(math.ceil(len(list_tocheck) / float(th_launch)))
    threads = []

    contar = 0

    for i in range(th_launch):
        t = Thread(
            target=auxiliar,
            args=(list_tocheck[chunksize * i: chunksize * (i + 1)],
                  final_list,
                  contar))

        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return final_list


def get_namespaces(rdf_path):
    my_namespaces = dict([node for _, node in ET.iterparse(
        os.open(str(rdf_path), os.O_RDONLY), events=['start-ns'])])
    return my_namespaces


def multiabstract_prepare(abs_list, threads=False):
    """
    Downloads the resource associated to each id on the list [after checking its existence]
    from elsevier API with  abstract retrieval, and returns an array of lists of two arguments: 1) the path to the rdf file
    and 2) a dictionary with its namespaces.
    :AG_repo_conn
    :return: a list made of sublists, each of containing
    """
    if threads == False:
        clean_list = threaded_checker(abs_list, req_type='abstr', th_launch=1)

    else:
        clean_list = threaded_checker(abs_list, req_type='abstr', th_launch=5)

    todo_list = []  # We will save here the responses of elsevier_interact to each article. A filepath.

    final_list = []

    for article_to_request in clean_list:
        article_ready = [elsevier_interact(article_to_request, 'abstr')]
        todo_list.append(article_ready)

    for article_info in todo_list:

        for article_path in article_info:
            local_ns = get_namespaces(article_path)
            final_list.append([article_path, local_ns])

    # At this point, todo_list has an array of lists containing a filepath and a dictionary with its namespaces.
    # We should start importing to the triple store each RDF file and making only one dictionary to add
    # all of the missing namespaces to the repository at the end.

    return final_list


def prefix_corrector(dict, old, new):
    """
    This function exists because we need to change the name of a given prefix in the dictionary which is to be uploaded to agraph database. So for a given namespace we change the prefix we think should be, before it is inserted in the triple store.
    :param dict: dictionary containing all of the prefixes and namespaces
    :param old: old prefix
    :param new: new prefix
    :return:
    """

    if old in dict:
        dict[new] = dict[old]
        del dict[old]


def multiabstract_insert(insert_list, repo_conn_obj):
    """
    We take a list of couples, each having a filepath and a dictionary with its prefixes and namespaces
    at the end we insert each file by path and upload the last version of the dictionary. Updated with each
    abstract RDF.

    :param insert_list: list of couples, a) a filepath to RDF file, and b) a dictionary like ns_dict.
        prefixes and namespaces.
    :param repo_conn_obj: repository connection object.
    :return:
    """

    ns_dict = {
        'err': '<http://www.w3.org/2005/xqt-errors#>',
        'fn': '<http://www.w3.org/2005/xpath-functions#>',
        'keyword': '<http://franz.com/ns/keyword#>',
        'nd': '<http://franz.com/ns/allegrograph/5.0/geo/nd#>',
        'ndfn': '<http://franz.com/ns/allegrograph/5.0/geo/nd/fn#>',
        'xs': '<http://www.w3.org/2001/XMLSchema#>',
        'xsd': '<http://www.w3.org/2001/XMLSchema#>',
        'dc': '<http://purl.org/dc/elements/1.1/>',
        'dcterms': '<http://purl.org/dc/terms/>',
        'foaf': '<http://xmlns.com/foaf/0.1/>',
        'fti': '<http://franz.com/ns/allegrograph/2.2/textindex/>',
        'owl': '<http://www.w3.org/2002/07/owl#>',
        'rdf': '<http://www.w3.org/1999/02/22-rdf-syntax-ns#>',
        'rdfs': '<http://www.w3.org/2000/01/rdf-schema#>',
        'skos': '<http://www.w3.org/2004/02/skos/core#>',
    }

    upload_dict = {}

    for couple in insert_list:
        repo_conn_obj.addFile(couple[0])
        upload_dict.update(couple[1])
        time.sleep(0.1)



    prefix_corrector(upload_dict, 'api', 'elsapi')

    for prefix in upload_dict.keys():
        if prefix not in ns_dict:
            repo_conn_obj.setNamespace(prefix, upload_dict[prefix])