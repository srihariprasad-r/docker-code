FROM postgres:latest
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=postgres
COPY sample.sql /docker-entrypoint-initdb.d/create_fixtures.sql