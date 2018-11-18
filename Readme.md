


search-ui -react app

to start the app
pip install -r requirements.txt
 ./start_dev.sh

 app will run on localhost:5000


scope of improvement
load the search and indexing part by another process and the flask app communicate to it via another port
add caching via redis to cache commonly used search keywords