from allegro_server import myrepo
import math
from threading import Thread
import json
from ast import literal_eval
from franz.openrdf.query.query import QueryLanguage

UNKNOWN = None
#esto es un comentario nuevo
NOISE = None
CORE = True
BORDER = False

#txt_locations = open('visual_interface/locations_latlng.txt', 'r').read()

pre_txt_locations = open('visual_interface/valle_cauca/js/locations.js', 'r').read()
txt_locations = pre_txt_locations.split('= ' )[1].split(';')[0]
print(type(txt_locations))
locations = literal_eval(txt_locations)
cluster_number = 1


def dbscan(input_nodes, minPts, eps):
    nodes_dictionary = {}

    active_nodes = []

    for node in input_nodes:
        active_nodes += [str(node)]

    repo_conn = myrepo()

    for node in active_nodes:
        nodes_dictionary[node] = {
            "evaluated": False,
            "node_type": NOISE,
            "cluster": 0
        }
    print(nodes_dictionary)
    main_launcher(repo_conn, nodes_dictionary, active_nodes, minPts, eps)
    print(nodes_dictionary)
    return nodes_dictionary

def main_launcher(repo_conn, nodes_dictionary, active_nodes, minPts, eps):
    global cluster_number

    cluster_number = 1

    def tempLinks_inserter(repo_conn, nodes_to_evaluate):

        def listThreads(repo_conn, in_list, th_launch, function_to_do):

            chunksize = int(math.ceil(len(in_list) / float(th_launch)))

            launched_threads = []

            for i in range(th_launch):
                t = Thread(
                    target=function_to_do,
                    args=(repo_conn, in_list[chunksize * i: chunksize * (i + 1)])
                )

                launched_threads.append(t)
                t.start()

            for t in launched_threads:
                t.join()
            print('threads ended')

        def tempQuery_inserter(repo_conn, in_list):
            for i in in_list:
                queryData = '<https://api.elsevier.com/content/affiliation/affiliation_id/%s> <http://www.gcarti.co/mc/geodata/link> "ongoingQuery" .' % (
                    i)
                print(queryData)
                repo_conn.addData(queryData)

        listThreads(repo_conn, nodes_to_evaluate, 10, tempQuery_inserter)

    def tempLinks_delete(repo_conn):
        delete_query = "DELETE { ?person glct:link 'ongoingQuery' } WHERE {?person glct:link 'ongoingQuery' }"

        repo_conn.executeUpdate(delete_query)

    def neighborsQuery(repo_conn, lat, lng, eps):
        queryString = """ SELECT DISTINCT ?afid {
                    ?affil nd:inCircle (glct:latlon_prueba_def keyword:lat %s keyword:lon %s keyword:radius %s keyword:units keyword:km).
                    ?affil elsapi:afid ?afid. 
                    ?affil glct:link 'ongoingQuery' . } """
        fullQuery = queryString % (lat, lng, eps)
        print(fullQuery)

        tuple_query = repo_conn.prepareTupleQuery(QueryLanguage.SPARQL,
                                                  fullQuery)  # preparar la consulta con la API
        result = tuple_query.evaluate()  # meter los resultados en variable

        affs = []  # arreglo para guardar cada afiliacion, su nombre y las apariciones en listas

        with result:
            for binding_set in result:
                afid = binding_set.getValue("afid")
                affs = affs + [afid]  # se agrega cada lista al arreglo affs
                # print("%s %s %s" % (s, p, o))
        print(affs)
        return (affs)

    def cluster_assigner(affil, local_neighbors, nodes_dictionary):
        global cluster_number
        for local_neighbor in local_neighbors:
            local_neighbor = str(local_neighbor).replace('"', '')
            if nodes_dictionary[local_neighbor]['cluster'] != 0:
                nodes_dictionary[affil]['cluster'] = nodes_dictionary[local_neighbor]['cluster']
                return
        nodes_dictionary[affil]['cluster'] = cluster_number
        cluster_number = cluster_number + 1

    def cluster_spreader(affil, local_neighbors, nodes_dictionary):
        for local_neighbor in local_neighbors:
            local_neighbor = str(local_neighbor).replace('"', '')
            if nodes_dictionary[local_neighbor]['cluster'] == 0:
                nodes_dictionary[local_neighbor]['cluster'] = nodes_dictionary[affil]['cluster']
                nodes_dictionary[local_neighbor]['node_type'] = 'BORDER'

    def node_evaluation(repo_conn, old_affil, minPts, eps, nodes_dictionary):

        affil = str(old_affil).replace('"', '')
        print('node eval ' + affil)
        if nodes_dictionary[affil]['evaluated'] == True:
            print('node_evaluated')
            return

        local_neighbors = neighborsQuery(repo_conn, locations[affil]['lat'], locations[affil]['lng'],
                                         eps)
        print(len(local_neighbors))
        print('local neigh on nodeEval ' + str(local_neighbors))

        nodes_dictionary[affil]['evaluated'] = True

        if len(local_neighbors) >= minPts:

            nodes_dictionary[affil]['node_type'] = CORE
            if nodes_dictionary[affil]['cluster'] == 0:
                cluster_assigner(affil, local_neighbors, nodes_dictionary)
            if nodes_dictionary[affil]['cluster'] != 0:
                cluster_spreader(affil, local_neighbors, nodes_dictionary)
            for local_neighbor in local_neighbors:
                node_evaluation(repo_conn, local_neighbor, minPts, eps, nodes_dictionary)

        elif len(local_neighbors) < minPts:
            if nodes_dictionary[affil]['node_type'] == NOISE:
                return

    print('Launching MAINQUERY')
    tempLinks_inserter(repo_conn, active_nodes)

    for affil in active_nodes:
        affil = str(affil).replace('"','')
        if nodes_dictionary[affil]['evaluated'] == True:
            print('node ' + affil+' already evaluated.')
        else:
            print('starting eval for ' + affil)
            node_evaluation(repo_conn, affil, minPts, eps, nodes_dictionary)

    tempLinks_delete(repo_conn)




###################### VINCENTy FOR LENGTh ###############

import math

# WGS 84
a = 6378137  # meters
f = 1 / 298.257223563
b = 6356752.314245  # meters; b = (1 - f)a

MILES_PER_KILOMETER = 0.621371

MAX_ITERATIONS = 200
CONVERGENCE_THRESHOLD = 1e-12  # .000,000,000,001


def vincenty_inverse(point1, point2, miles=False):
    """
    Vincenty's formula (inverse method) to calculate the distance (in
    kilometers or miles) between two points on the surface of a spheroid
    """

    # short-circuit coincident points
    if point1[0] == point2[0] and point1[1] == point2[1]:
        return 0.0

    U1 = math.atan((1 - f) * math.tan(math.radians(point1[0])))
    U2 = math.atan((1 - f) * math.tan(math.radians(point2[0])))
    L = math.radians(point2[1] - point1[1])
    Lambda = L

    sinU1 = math.sin(U1)
    cosU1 = math.cos(U1)
    sinU2 = math.sin(U2)
    cosU2 = math.cos(U2)

    for iteration in range(MAX_ITERATIONS):
        sinLambda = math.sin(Lambda)
        cosLambda = math.cos(Lambda)
        sinSigma = math.sqrt((cosU2 * sinLambda) ** 2 +
                             (cosU1 * sinU2 - sinU1 * cosU2 * cosLambda) ** 2)
        if sinSigma == 0:
            return 0.0  # coincident points
        cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLambda
        sigma = math.atan2(sinSigma, cosSigma)
        sinAlpha = cosU1 * cosU2 * sinLambda / sinSigma
        cosSqAlpha = 1 - sinAlpha ** 2
        try:
            cos2SigmaM = cosSigma - 2 * sinU1 * sinU2 / cosSqAlpha
        except ZeroDivisionError:
            cos2SigmaM = 0
        C = f / 16 * cosSqAlpha * (4 + f * (4 - 3 * cosSqAlpha))
        LambdaPrev = Lambda
        Lambda = L + (1 - C) * f * sinAlpha * (sigma + C * sinSigma *
                                               (cos2SigmaM + C * cosSigma *
                                                (-1 + 2 * cos2SigmaM ** 2)))
        if abs(Lambda - LambdaPrev) < CONVERGENCE_THRESHOLD:
            break  # successful convergence
    else:
        return None  # failure to converge

    uSq = cosSqAlpha * (a ** 2 - b ** 2) / (b ** 2)
    A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
    B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))
    deltaSigma = B * sinSigma * (cos2SigmaM + B / 4 * (cosSigma *
                 (-1 + 2 * cos2SigmaM ** 2) - B / 6 * cos2SigmaM *
                 (-3 + 4 * sinSigma ** 2) * (-3 + 4 * cos2SigmaM ** 2)))
    s = b * A * (sigma - deltaSigma)

    s /= 1000  # meters to kilometers
    if miles:
        s *= MILES_PER_KILOMETER  # kilometers to miles

    return round(s, 6)