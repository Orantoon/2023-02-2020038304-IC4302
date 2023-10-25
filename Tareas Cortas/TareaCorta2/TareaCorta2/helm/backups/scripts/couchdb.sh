#!/bin/bash
DATE=$(date '+%Y%m%d%H%M')

mkdir -p /couchdbdump/$DATE

yum install -y yum-utils

yum-config-manager --add-repo https://couchdb.apache.org/repo/couchdb.repo
cat <<EOT > /etc/yum.repos.d/apache-couchdb.repo
[couchdb]
name=couchdb
baseurl=https://apache.jfrog.io/artifactory/couchdb-rpm/el9Server/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://couchdb.apache.org/repo/keys.asc https://couchdb.apache.org/repo/rpm-package-key.asc
EOT

yum update
#Consulta para obtener todos los documentos de la base de datos
curl -X GET -u admin:$COUCHDB_PASSWORD http://databases-couchdb:5984/couchdb/_all_docs?include_docs=true > /couchdbdump/$DATE/backup.json
#Muestra el contenido del archivo
cat /couchdbdump/$DATE/backup.json
#Sube el archivo al bucket AWS
aws s3 cp /couchdbdump/$DATE/ s3://$BUCKET_NAME/$BACKUP_PATH/ --recursive
#Muestra el contenido del bucket
aws s3 ls s3://$BUCKET_NAME/$BACKUP_PATH/
#Elimina el directorio temporal
rm -rf /couchdbdump/$DATE
