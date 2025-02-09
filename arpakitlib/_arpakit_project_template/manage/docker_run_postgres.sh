cd ..
source .env
docker rm ${project_name}_postgres
docker run --name ${project_name}_postgres -d -p ${sql_db_port}:5432 -e POSTGRES_USER=${sql_db_user} -e POSTGRES_PASSWORD=${sql_db_password} -e POSTGRES_DB=${sql_db_database} postgres:16 -c max_connections=100
docker start ${project_name}_postgres