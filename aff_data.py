import os
import re
from urllib.parse import quote
from xml.etree import ElementTree as ET
import json
import requests

import tech
import unicodedata
import personal
import math
from threading import Thread
from urllib.request import FancyURLopener
from get_data import elsevier_interact, threaded_checker
from personal import setenvar


def listmaker(clean_list, th_launch=1):
    """
We need to make the objects that will be inserted to the database. The inputs are


    HERE. WE NEED TO LAUNCH IN THREADS THE CLASS ELSAFI, each id for each aff is deployed and we reunite the resultant objects in clean_list
    :param clean_list:
    :param th_launch: default threads to launch is 1
    :return:
    """

    aff_obj_list = []

    def auxiliar(matrix, final_list):

        for affiliation in matrix:
            final_list.append(
                elsaffi(
                    str(affiliation[1]).replace('"', "")
                )
            )

    chunksize = int(math.ceil(len(clean_list) / float(th_launch)))
    threads = []

    contar = 0

    for i in range(th_launch):

        t = Thread(
            target=auxiliar,
            args=(clean_list[chunksize * i : chunksize * (i + 1)],
                  aff_obj_list)
        )

        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return aff_obj_list

class elsaffi(object):

    """
    Is a class that takes only one argument and construct

    """

    def __init__(self, affid):

        info = scopusaff(affid)  # we use scopusaff, a function that takes an aff id and
        #  returns a dictionary with name, city, country, postcode, state, address, lat, lng,
        # administrative areas level 1 and 2.
        self.affid = affid
        self.name = info['name']  # skos:prefLabel
        self.city = info['city']  # glct:city
        self.country = info['country']  # glct: country

        try:
            self.postcode = info['postal_code']  # glct: post_code
        except (LookupError, AttributeError):
            mk_msg = affid + ' has no postal code'
            tech.report_log(mk_msg, 'missing_information')


        self.address = info['address']  # glct: addr
        self.lat = info['lat'] # glct: lat
        self.lng = info['lng'] # glct: lon
        try:
            self.aal1 = info['ad_area_lvl_1']  # glct: aal_1
        except (LookupError, AttributeError):
            mk_msg = affid + ' has no ad area lvl 1'
            tech.report_log(mk_msg, 'missing_information')

        try:
            self.aal2 = info['ad_area_lvl_2'] # glct: aal_2
        except (LookupError, AttributeError):
            mk_msg = affid + ' has no ad area lvl 2'
            tech.report_log(mk_msg, 'missing_information')
        print(info)

    def value_export(self, valuename):

        if valuename == 'address':
            return self.address
        elif valuename == 'city':
            return self.city
        elif valuename == 'country':
            return self.country
        elif valuename == 'postcode':
            if hasattr(self, 'postcode'):
                return self.postcode
            else:
                return 'N/A'

        elif valuename == 'lat':
            return self.lat
        elif valuename == 'lng':
            return self.lng
        elif valuename == 'aal_1':
           if hasattr(self, 'aal1'):
               return self.aal1
           else:
               return 'N/A'

        elif valuename == 'aal_2':
            if hasattr(self, 'aal2'):
                return self.aal2
            else:
                return 'N/A'

def batch_processing(aff_obj_list, repo_conn_object):
    """
    We take the list of affiliations objects which contain all of the info for each affiliation.
    On the list 'triples ready' we will storage lists each representing a triple to insert.
    Each affiliation will have a number of triples on 'triples ready', one triple for each property that will be inserted.

    We need to process a full batch of objects containing each one the information form each affiliation. We need to transform those objects to triples so we process them until we have the triples.

    Each triple is of the form:

            <university complete URI> <property URI> <literal value exported from object>.

    :param aff_obj_list: List with the objects representing each an affiliation an its metadata
    :param repo_conn_object: the object repo connection
    :return: insert the triples to agraph repo through repo_conn_object
    """

    repo_conn_object.setNamespace('glct', 'http://www.gcarti.co/mc/geodata/')
    repo_conn_object.setNamespace('tags', 'http://www.gcarti.co/mc/tags/')

    properties = ['city',
                  'country',
                  'postcode',
                  'address',
                  'lat',
                  'lng',
                  'aal_1',
                  'aal_2',
                  'latlon_prueba_def',
                  'tagger'
                  ]
    gcarti_prefix = '<http://www.gcarti.co/mc/geodata/'

    def segment_processer(aff_obj_list_segment):
        for each_aff in aff_obj_list_segment:

            aff_ref = '<https://api.elsevier.com/content/affiliation/affiliation_id/'

            s = aff_ref + each_aff.affid + '>'

            for aff_prop in properties:

                p = gcarti_prefix + aff_prop +'>'

                # THIS IS OUR CORE GEO-INDEXING AND TAG REQUEST FROM OPENSTREETMAPS. INSTERTS THEM ON THE FLY

                if aff_prop == 'latlon_prueba_def':

                    l_lat = float(each_aff.value_export('lat'))
                    l_lon = float(each_aff.value_export('lng'))

                    o_prev = '"&lat=' + str(l_lat) + '&lon=' + str(l_lon)
                    o_toformat = o_prev + '"^^<http://franz.com/ns/allegrograph/5.0/geo/nd#_lat_la_-9.+1_+9.+1_+1.-4_+1.-3_lon_lo_-1.8+2_+1.8+2_+1.-4> .'

                    o = o_toformat.replace("'", '')
                    print(o)

                    repo_conn_object.addData(s + ' ' + p + ' ' + o)

                elif aff_prop == 'tagger':

                    to_add = []

                    aff_tag_assigner(s, tagger_filePath(each_aff.affid, l_lat, l_lon), to_add)

                    print(to_add)
                    for triple in to_add:
                        print(triple)
                        repo_conn_object.addData(triple)

                else:

                    o = each_aff.value_export(aff_prop)
                    print('S is %s, P is %s, O is %s' % (s, p, o))
                    repo_conn_object.addData(s +'' +p+' "'+ o+'" .')

    th_launch = 6

    chunksize = int(math.ceil(len(aff_obj_list) / float(th_launch)))
    ### I COULD TRY INSERTING THREADS HERE SO IT WON'T TAKE SO LONG BYT MAYBE IT'LL BRAKE THE CONNECTION
    threads = []

    for i in range(th_launch):
        t = Thread(
            target=segment_processer,
            args=([aff_obj_list[(chunksize * i):(chunksize * (i + 1))]])
        )

        threads.append(t)
        t.start()

    for t in threads:
        t.join()






    #repo_conn_object.addTriples(triples_ready)

def tagger_filePath(affid, l_lat, l_lon):

    try:

        full_path = 'files/osm/json/' + affid + '.json'
        open(full_path, 'r')

        return full_path

    except FileNotFoundError:

        google_maps_apikey = setenvar(req='GOOGLE_MAPS_APIKEY')

        #base_url = 'https://nominatim.openstreetmap.org/reverse?format=jsonv2&'

        base_url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + str(l_lat) + ',' + str(l_lon) + \
        '&key=' + google_maps_apikey

        #url_suf = 'lat=' + str(l_lat) + '&lon=' + str(l_lon)

        osm_response = requests.get(base_url)

        if str(osm_response) == '<Response [200]>':

            print(affid + ' file OK from OSM.')

            tosave = str(osm_response.text.encode('utf-8').decode('utf-8', 'ignore'))  # make tree from

            f = open(full_path, "w+")
            f.write(str(tosave))

            return full_path

def aff_tag_assigner(s, file_path, to_add):
    properties = {"administrative_area_level_2": {"long_name": "city"},
                  "administrative_area_level_1": {"long_name": "state"},
                  "country": {"long_name": "country", "short_name": "code"}}
    p_pre = '<http://www.gcarti.co/mc/tags/'

    with open(file_path) as f:
        data = json.load(f)
        print(data)
        for property in properties.keys():
            property_present = False
            try:
                for element in data['results'][0]['address_components']:
                    if property in element['types']:
                        property_present = True
                        for value_to_extract in properties[property].keys():
                            #print(property, ' ', value_to_extract, ' ', element[value_to_extract])
                            #print(properties[property][value_to_extract])
                            p = p_pre + properties[property][value_to_extract] +'>'
                            to_add.append(s + ' ' + p + ' ' + '"' + element[value_to_extract] + '" .')
                    elif 'locality' in element['types']:
                        property_present = True
                        p = p_pre + 'city>'
                        to_add.append(s + ' ' + p + ' ' + '"' + element['long_name'] + '" .')
            except:
                message = s + ' not being geocoded as no results were retrieved '
                tech.report_log(message=message, log='errorlog.txt')
            if not property_present:
                message = property + ' not present for ' + s
                tech.report_log(message=message, log='missing_tags.txt')

def enelmapa(busqfin):

    class MyOpener(FancyURLopener):
        version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

    def strip_accents(s):
        return ''.join(c for c in unicodedata.normalize('NFD', s)
                       if unicodedata.category(c) != 'Mn')


    personal.setenvar(proxy=False)
    print('Searching directly on Google Maps MAP')
    myopener = MyOpener()
    busqfin = strip_accents(busqfin)
    page = myopener.open('http://www.google.com/maps?q=' + busqfin)
    print('http://www.google.com/maps?q=' + busqfin)
    prueba = page.read()
    a = str(prueba)
    print(a)

    first_string = a[a.find('center=')+7:a.find('center=') + 80]
    lat = first_string[0:first_string.find('%2C')]
    lon = first_string[first_string.find('%2C')+3:first_string.find('&amp')]

    # print('latlon ', lat, lon)

    latlon = [float(lat), float(lon)]
    print(latlon)

    return latlon

def scopusaff(id):  # this function takes an scopus affiliation ID and returns name, address, city
    # then we look up that name in setcoord and join the  two dictionaries.
    # setenvar() # function to set environment variables

    aff_file = elsevier_interact(id, req_type='affil')

    temproot = ET.parse(aff_file)

    dict_data = {'name': temproot.find('affiliation-name').text}

    for affprofile in temproot.findall('institution-profile'):
        print(id)
        dict_data['address'] = ''
        dict_data['city'] = ''
        dict_data['country'] = ''
        dict_data['id'] = id

        for physaddress in affprofile.findall('address'):

            try:
                dict_data['address'] = physaddress.find('address-part').text
            except AttributeError:
                print('Requesting GEOCODING without "address" parameter for ' + id)
                dict_data['address'] = ''

            try:
                dict_data['city'] = physaddress.find('city').text
            except AttributeError:
                print('Requesting GEOCODING without "city" parameter for ' + id)
                dict_data['city'] = ''

            try:
                dict_data['country'] = physaddress.find('country').text
            except AttributeError:
                print('Requesting GEOCODING without "country" parameter for' + id)
                dict_data['country'] = ''

    geocode_dict = {}

    geocode(dict_data=dict_data, data_return=geocode_dict)

    dict_data.update(geocode_dict)

    return dict_data

def multiaff_prepare(affs_list, threads=False):
    """
    Take a list with affiliations IDs and check them through threaded_checker,
    which uses elsevier_interact. It returns a clean list with only the affiliations
    that were found on SCOPUS database. The files are downloaded while checking [elsevier_interact behavior].

    It then makes an array from clean list containing couples of the form [name, Scopus_id].

    returns it in return_list

    :param affs_list: first list retrieved from agraph database, affiliations IDs to be checked on SCOPUS.
    :threads: if TRUE it launches threaded_checker with 5 threads. Only with 1 otherwise.
    :return: Clean list with successfully found/retrieved resources associated with an ID on affs_list.
    """
    th_launch = 1
    ids_list = []
    return_list = []

    if threads == True:
        th_launch = 5

    for affil in affs_list:
        ids_list.append(str(affil[1]).replace('"', ""))

    ready_list = threaded_checker(ids_list, 'affil', th_launch=th_launch)

    for affil_id in ready_list:
        for affil in affs_list:
            if affil_id == str(affil[1]).replace('"', ""):
                return_list.append([affil[0], affil_id])

    return return_list

def geocode(dict_data, re_run=False, latlon=False, data_return={}):
    """
    We need to geocode each affiliation. This functions is needed because it makes 3 runs trying to find the geopoint. The first run is made on google maps API with name, address, city and country; if it doesn't work we then search without address parameter; if it still doesn't work we try to look on google maps webpage search bar and retreive the latitude and longitude.

    :param dict_data: is a dictionary containing all the info from the place to geocode.
                    keys are: name, address, city, country
    :param re_run:
    :param latlon:
    :param data_return:
    :return:
    """
    setenvar(proxy=False)
    google_maps_apikey = os.environ.get('GOOGLE_MAPS_APIKEY')

    search_pref = 'https://maps.googleapis.com/maps/api/geocode/xml?'

    if not re_run:

        search_term = dict_data['name'] + '+' + dict_data['address'] + '+' + dict_data['city'] + '+' + dict_data[
            'country']

    else:
        if latlon:

            search_term = dict_data['name']

        else:

            search_term = dict_data['name'] + '+' + dict_data['city'] + '+' + dict_data['country']

    if not latlon:

        url_encode = re.sub("%2B", "+", re.sub("%20", "+", quote(search_term)))

        searchready = search_pref + 'address=' + url_encode + '&key=' + google_maps_apikey

    else:

        maps_latlon = enelmapa(search_term)

        searchready = search_pref + 'latlng=' + str(maps_latlon[0]) + ',' + str(maps_latlon[1]) + \
                      '&key=' + google_maps_apikey

    print('Geocode request  ' + searchready)

    geocodeapi_response = requests.get(searchready, proxies={'http': '', 'https': ''})

    toprint = geocodeapi_response.text.encode('UTF-8')



    temproot = ET.fromstring(toprint)

    if temproot.find('status').text == 'OK':
        print('Xml ok from Google Maps API')

        for result in temproot.findall('result'):

            for geometry in result.findall('geometry'):
                for location in geometry.findall('location'):
                    data_return['lat'] = location.find('lat').text
                    data_return['lng'] = location.find('lng').text

            for address_comp in result.findall('address_component'):
                if address_comp.find('type').text == 'postal_code':
                    data_return['postal_code'] = address_comp.find('long_name').text

                if address_comp.find('type').text == 'administrative_area_level_1':
                    data_return['ad_area_lvl_1'] = address_comp.find('long_name').text

                if address_comp.find('type').text == 'administrative_area_level_2':
                    data_return['ad_area_lvl_2'] = address_comp.find('long_name').text

                return

    elif temproot.find('status').text == 'ZERO_RESULTS':

        if latlon:
            mk_msg = 'We still don\'t find that place, even on the browser map' + dict_data[
                'id'] + '. We\'ll make a last try searching only by name'

            tech.report_log(mk_msg, 'missing_information')

            geocode(dict_data, latlon=True, re_run=True, data_return=data_return)

        else:

            if not re_run:

                mk_msg = 'no results from Google Maps Api for ' + dict_data[
                    'id'] + '. Will re run without address parameter on the search string'

                tech.report_log(mk_msg, 'missing_information')

                print(
                    'No results, re run will be made without address parameter on the search string request')

                geocode(dict_data, re_run=True, data_return=data_return)

            else:

                mk_msg = 'no results from Google Maps Api for ' + dict_data[
                    'id'] + ' in the 2nd try. Will try method to get it from Google Maps website.'

                tech.report_log(mk_msg, 'missing_information')

                geocode(dict_data, latlon=True, data_return=data_return)

    else:
        print(temproot.find('status').text)
        return