docker rm arpakitlib_postgres
docker run --name arpakitlib_postgres -d -p 50629:5432 -e POSTGRES_USER=arpakitlib -e POSTGRES_PASSWORD=arpakitlib -e POSTGRES_DB=arpakitlib postgres:16 -c max_connections=100
docker start arpakitlib_postgres