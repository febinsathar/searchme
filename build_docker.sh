docker build -t search_me .


docker run -d --name search_me search_me -p 5000:5000
