from flask import Flask
from flask import request
from ast import literal_eval
from dbscan import dbscan



app = Flask(__name__)
#app.secret_key = 's3cr3t'
#app.debug = True
#app._static_folder = os.path.abspath("templates/static/")


@app.route('/dbscan_cluster', methods=['GET'])
def index():
    if request.method == 'GET':
        nodesList = request.args.get('nodesList')
        minPts = int(request.args.get('minPts'))
        eps = int(request.args.get('eps'))
        toReturn = str(type(nodesList))
        print(toReturn)
        affiliations_to_cluster = literal_eval(nodesList)
        print(type(affiliations_to_cluster))
        returnDict = dbscan(affiliations_to_cluster, minPts, eps)
        return str(returnDict).replace('True','"core"').replace('None','"Noise"').replace('False','"Border"').replace("'",'"').replace(" ","")

if __name__ == "__main__":
	app.run()

