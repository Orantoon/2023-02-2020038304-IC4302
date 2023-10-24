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
yum install jq -y
jq --version 
CURRENT_REV=$(curl -s -X GET "$COUCHDB_URL/$DB_NAME/$DOCUMENT_ID" | jq -r '._rev')

aws s3 cp s3://$BUCKET_NAME/$BACKUP_PATH/ /backup/ --recursive
jq  '{docs: [.rows[].doc]}' ../backup/backup.json > documentos.json
cat documentos.json
curl -X POST -d @"documentos.json" -H "Content-Type: application/json" -u admin:$COUCHDB_PASSWORD 10.1.7.17:5984/couchdb/_bulk_docs

rm -rf /backup/