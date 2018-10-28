import os
import tech

def setenvar(putv=None, req=None, proxy=True):
    """
    We need to set all the environmental variables to use our application, that because we are outside the server network and the authorized network to download files from SCOPUS.
    We need to set the correct proxy [we use a socks proxy on a ssh tunnel to connect to univalle server], agraph user, password, host, and port. Which will be used as default unless we specify another value on the procedures at exectuion time.

    We also need to set the correct apikeys as environment because they are used in different scenarios.

    :param putv: when we pass a dictionary containing environmental variables names and values, those are joint with the main dictionary before setting the variables.
    :param req: if we request a variable which is contained in the main dictionary [environ_dict], then the function returns it, otherwise it tells us doesn't exist.
    Otherwise when no request is made the environmental variables are SET.
    :return:
    """

    MACHINE = tech.hostname

    ELSEVIER_APIKEY = '8549a609d6e7719c80e796018d29e5d4'
    GOOGLE_MAPS_APIKEY = 'AIzaSyDfY9hPl2RGTTSO28r62l6ORwJxIkTCt4U'
    HTTP_PROXY = 'socks5h://127.0.0.1:21331'
    HTTPS_PROXY = "socks5h://127.0.0.1:21331"
    AGRAPH_USER = 'user'
    AGRAPH_PASSWORD = 'mio'
    AGRAPH_HOST = 'localhost'
    AGRAPH_PORT = '10035'
    ERROR_LOG_PATH = '/'

    if MACHINE == 'geolocarti':
        HTTP_PROXY = ''
        HTTPS_PROXY = ''

    environ_dict = {
                    'ELSEVIER_APIKEY' : ELSEVIER_APIKEY,
                    'GOOGLE_MAPS_APIKEY' : GOOGLE_MAPS_APIKEY,
                    'HTTP_PROXY' : HTTP_PROXY,
                    'HTTPS_PROXY' : HTTPS_PROXY,
                    'AGRAPH_USER' : AGRAPH_USER,
                    'AGRAPH_PASSWORD' : AGRAPH_PASSWORD,
                    'AGRAPH_HOST' : AGRAPH_HOST,
                    'AGRAPH_PORT' : AGRAPH_PORT
                    }

    if type(putv) == dict:

        environ_dict.update(putv)

    if proxy == False:
        environ_dict['HTTPS_PROXY']=''
        environ_dict['HTTP_PROXY']=''

    if req == None:

        os.environ["ELSEVIER_APIKEY"] = environ_dict['ELSEVIER_APIKEY']
        os.environ["GOOGLE_MAPS_APIKEY"] = environ_dict['GOOGLE_MAPS_APIKEY']

        os.environ["HTTP_PROXY"] = environ_dict["HTTP_PROXY"]
        os.environ["HTTPS_PROXY"] = environ_dict['HTTPS_PROXY']

        os.environ["AGRAPH_USER"] = environ_dict['AGRAPH_USER']
        os.environ["AGRAPH_PASSWORD"] = environ_dict['AGRAPH_PASSWORD']
        os.environ["AGRAPH_PORT"] = environ_dict['AGRAPH_PORT']
        os.environ["AGRAPH_PROXY"] = environ_dict['HTTP_PROXY']
        os.environ["AGRAPH_HOST"] = environ_dict['AGRAPH_HOST']

    elif req in environ_dict:

        return environ_dict[req]
    else:

        'Environment variable not specified'


