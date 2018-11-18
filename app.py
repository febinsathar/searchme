from flask import Flask,request,jsonify,send_from_directory

from flask_cors import CORS, cross_origin
from dynaconf import FlaskDynaconf



import pandas as pd
import os
import timeit
from search.ngramPandas import NgramPandas

APP_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_FOLDER = os.path.join(APP_DIR, 'search-ui/build/')

app = Flask(__name__, static_folder=STATIC_FOLDER)
FlaskDynaconf(app)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


data =pd.read_csv('data/word_search.tsv', sep='\t',header=None,names=['word', 'freq'])
ngram =NgramPandas(data)

# Serve React App index
@app.route('/')
def render_app():
    return send_from_directory('search-ui/build', 'index.html')

@app.route('/ping')
def ping():
    return jsonify({"ping":"pong"}) , 400

@app.route('/static/<path:path>') # Serve whatever the client requested in the static folder
def serve_static(path):
    return send_from_directory('search-ui/build/static/', path)

@cross_origin()
@app.route("/search")
def search():

    search_term = request.args.get('word', default = '*', type = str).lower()
    page_start = request.args.get('page_start', default = 0, type = int)
    page_end = request.args.get('page_end', default = 25, type = int)

    if(not search_term.isalpha()):
       return jsonify({"error":"search engine supports only alphabets"}) , 400 

    if(page_start>=page_end):
        return jsonify({"error":"page start should be greater than page end"}) , 400

    if(search_term==""):
        return jsonify({"result":[],"total":0,"time":"0s"})
    
    try:
        start = timeit.default_timer()
        result=ngram.search_me(search_term)
        stop = timeit.default_timer()
        total_records=result.shape[0]
        page_start= 0 if(page_start)<0 else page_start
        page_end=total_records if (page_end>total_records) else page_end
        resp = result.iloc[page_start:page_end].reset_index()[['word','freq','score']].to_dict(orient='records')
        return jsonify({"result":resp,"totalRecords":result.shape[0],"time":str(round(stop - start, 5))+"s","pageStart":page_start,"pageEnd":page_end}), 200
    except Exception as e:
        return jsonify({"error":str(e)}) , 400


