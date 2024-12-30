cd ..
docker rm ..._postgres
docker run --name ..._postgres -d -p ...:5432 -e POSTGRES_USER=... -e POSTGRES_PASSWORD=... -e POSTGRES_DB=... postgres:16 -c max_connections=100
docker start ..._postgres