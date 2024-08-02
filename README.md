# taxi-api-v2

Create and run the container for postgres

docker run --name some-postgres -p 5432:5432 \
    -e POSTGRES_USER=taxi -e POSTGRES_DB=taxi -e POSTGRES_PASSWORD=taxi -d postgres

Create and run the container for redis

docker run --name some-redis -p 6379:6379 -d redis
