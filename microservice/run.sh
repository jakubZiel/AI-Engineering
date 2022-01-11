#check if microservice/mongodb/database folder exists
cd mongodb

docker-compose up -d

pwd

cd ..

python3 server.py

cd mongodb

docker-compose down