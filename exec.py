import get_data
from allegro_server import myrepo
from init_config.list import init_list, abstract_list_1, abstract_list_2
from init_config import html_maker
import allegro_interact
import aff_data


print(init_list)

repo_conn = myrepo(host='127.0.0.1', repo='virtual_sep17')

"""
abstracts_prepared_list = get_data.multiabstract_prepare(init_list, threads=True)

#abstracts_prepared_list = get_data.multiabstract_prepare(abstract_list_1[0:999], threads=True)
#abstracts_prepared_list = get_data.multiabstract_prepare(abstract_list_1[1000:1999], threads=True)
#abstracts_prepared_list = get_data.multiabstract_prepare(abstract_list_1[2000:2999], threads=True)
abstracts_prepared_list = get_data.multiabstract_prepare(abstract_list_1[3000:3999], threads=True)

#abstracts_prepared_list = get_data.multiabstract_prepare(abstract_list_1[4000:4999], threads=True)
#abstracts_prepared_list = get_data.multiabstract_prepare(abstract_list_1[5000:5999], threads=True)
#abstracts_prepared_list = get_data.multiabstract_prepare(abstract_list_1[6000:6999], threads=True)
#abstracts_prepared_list = get_data.multiabstract_prepare(abstract_list_1[7000:7999], threads=True)
#abstracts_prepared_list = get_data.multiabstract_prepare(abstract_list_1[8000:], threads=True)

#abstracts_prepared_list = get_data.multiabstract_prepare(abstract_prepared_list2, threads=True)

"""
"""
print(abstracts_prepared_list)

print('Inserting articles RDF metadata triples to rdf database')

get_data.multiabstract_insert(abstracts_prepared_list, repo_conn)

repo_conn.deleteDuplicates('spo')  # At this point the repository is without duplicate statements.

print('Triples on reference to the articles have been successfully loaded.')

"""
### HERE WE NEED TO BRAKE AND GET ONLY THOSE WHO FALTAN
affs_raw_list = (allegro_interact.aff_count_query(repo_conn))
repo_conn.deleteDuplicates('spo')
print('Make CLEAN LIST')
### HERE WE NEED TO BRAKE AND GET ONLY THOSE WHO FALTAN

affs_clean_list = aff_data.multiaff_prepare(affs_raw_list, threads=True)

# At this point there is a list with only the affiliations which resources were effectively found on SCOPUS.
# Files are downloaded while checking.

repo_conn.deleteDuplicates('spo')
print('Make OBJECTS LIST')

aff_object_list = aff_data.listmaker(affs_clean_list, th_launch=30)

#We pass the list with only the resources succesfully downloaded from elsevier.
#logs contain ids that have been discarded, for affiliations and full requested metadata from articles.
repo_conn.deleteDuplicates('spo')

print('Start BATCH PROCESSING')

aff_data.batch_processing(aff_object_list, repo_conn) #insert triples

print('ALL INFORMATION WAS GEO-INDEXED AND TAGGED. GLCT FULFILLED')


approved_nodes =[]
repo_conn.deleteDuplicates('spo')

print('starting allegro_interact.allInfo_query')
places = allegro_interact.allInfo_query(repo_conn, approved_nodes=approved_nodes)

path = 'visual_interface/places.txt'
places_locations = open(path,'w')
places_locations.write(str(places))

print('approved nodes_ EXEC_ ' + str(approved_nodes))

repo_conn.deleteDuplicates('spo')
weighted_links = allegro_interact.links_weighted(repo_conn, approved_nodes=approved_nodes) # Here we make the first network.

path = 'visual_interface/links.txt'
places_locations = open(path,'w')
places_locations.write(str(weighted_links))

allegro_interact.weighted_links_inserter(weighted_links,repo_conn)

repo_conn.deleteDuplicates('spo')