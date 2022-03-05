FROM mysql:latest

ENV MYSQL_DATABASE sample_db
ENV MYSQL_USER sample_user
ENV MYSQL_PASSWORD sample_password
ENV MYSQL_ROOT_PASSWORD euns@ur

COPY ./init.sql /docker-entrypoint-initdb.d/init.sql