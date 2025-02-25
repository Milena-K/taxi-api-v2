# taxi-api-v2

### You will need env variables for:
- SECRET_KEY
- DB_USER
- DB_PASSWORD
- DB_HOST
- DB_PORT

### Create and run the container for postgres

"""docker run --name taxi-postgres -p 5432:5432 \
-e POSTGRES_USER=taxiadmin -e POSTGRES_DB=taxidb -e POSTGRES_PASSWORD=taxi -d postgres"""

### Create and run the container for redis

"""docker run --name taxi-redis -p 6379:6379 -d redis"""

### Run celery from root folder

"""celery -A api worker -l INFO"""
