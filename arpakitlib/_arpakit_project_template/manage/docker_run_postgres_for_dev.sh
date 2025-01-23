cd ..
docker rm {{PROJECT_NAME}}_postgres
docker run --name {{PROJECT_NAME}}_postgres -d -p {{SQL_DB_PORT}}:5432 -e POSTGRES_USER={{PROJECT_NAME}} -e POSTGRES_PASSWORD={{PROJECT_NAME}} -e POSTGRES_DB={{PROJECT_NAME}} postgres:16 -c max_connections=100
docker start {{PROJECT_NAME}}_postgres