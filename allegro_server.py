from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.repository.repository import Repository
import tech
import personal


virtual_server_name = 'geolocarti'

def myrepo(host='127.0.0.1', repo='virtual_sep17'):
    personal.setenvar(proxy=False)

    print('Connecting to AllegroGraph [' + virtual_server_name +'] from ' + tech.hostname)

    server = AllegroGraphServer(host=host)

    catalog = server.openCatalog(name=None)  # abir catalogo que contiene el repositorio. Por defecto se abre  el catalogo llamado -system-
    print('catalog ', catalog.getName(), ' open')
    mode = Repository.OPEN
    my_repository = catalog.getRepository(repo, mode)  # abrir el repositorio
    my_repository.initialize()  # inicializar el repositorio

    repo_conn = my_repository.getConnection()
    print('Repository - %s - is up!' % my_repository.getDatabaseName())
    print('It contains %d statement(s).' % repo_conn.size())

    print('============================================ ======')

    repo_conn.disableDuplicateSuppression()

    return repo_conn

# consulta en SPARQL a variable

#myrepo()