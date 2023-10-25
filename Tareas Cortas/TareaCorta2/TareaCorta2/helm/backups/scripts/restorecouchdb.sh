#!/bin/bash 
mkdir -p /backup/
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
#Instala jq para poder parsear el json
yum install jq -y

#Copiar los archivos del bucket a la carpeta temporal
aws s3 cp s3://$BUCKET_NAME/$BACKUP_PATH/ /backup/ --recursive
#Parsea el json y lo guarda en  documentos.json
jq  '{docs: [.rows[].doc]}' ../backup/backup.json > documentos.json
#Muestra el contenido del archivo
cat documentos.json
#Sube los documentos a la base de datos
curl -X POST -d @"documentos.json" -H "Content-Type: application/json" -u admin:$COUCHDB_PASSWORD http://databases-couchdb:5984/couchdb/_bulk_docs
#Elimina el directorio temporal
rm -rf /backup/