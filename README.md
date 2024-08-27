# tcc2


# build the containers:
    docker-compose build

# run the container:
    docker-compose up

# Acess the running flask server container:
    docker exec -it tcc2-web-1 /bin/sh

# Acess the running database container:
    docker exec -it tcc2-db-1 psql -U user -d mydatabase