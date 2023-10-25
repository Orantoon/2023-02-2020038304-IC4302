#!/bin/bash
DATE=$(date '+%Y%m%d%H%M')

mkdir -p ~/tmp/postgredump/$DATE

yum update
amazon-linux-extras install postgresql14

# Realiza el respaldo de la base de datos PostgreSQL en el contenedor del pod de Kubernetes
PGPASSWORD=root pg_dump -h databases-postgresql -U root -d postgreDB -f ~/tmp/postgredump/$DATE/backup_postgre.sql

# Sube el respaldo a Amazon S3
aws s3 cp ~/tmp/postgredump/$DATE s3://tec-ic4302-02-2023/2022437529/postgresql/ --recursive

# Lista los archivos en el bucket de S3
aws s3 ls s3://tec-ic4302-02-2023/2022437529/postgresql/

# Limpia los archivos temporales
rm -rf ~/tmp/postgredump/$DATE


