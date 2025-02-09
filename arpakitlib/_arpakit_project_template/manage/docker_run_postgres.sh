cd ..
source .env
docker rm ${PROJECT_NAME}_postgres
docker run --name ${PROJECT_NAME}_postgres -d -p ${SQL_DB_PORT}:5432 -e POSTGRES_USER=${SQL_DB_USER} -e POSTGRES_PASSWORD=${SQL_DB_PASSWORD} -e POSTGRES_DB=${SQL_DB_DATABASE} postgres:16 -c max_connections=100
docker start ${PROJECT_NAME}_postgres