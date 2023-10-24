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
curl -X GET -u admin:2CU2iFr6m2auqNFJKlvO http://10.1.6.217:5984/couchdb/_all_docs?include_docs=true > /couchdbdump/$DATE/backup.json
cat /couchdbdump/$DATE/backup.json
aws s3 cp /couchdbdump/$DATE/ s3://$BUCKET_NAME/$BACKUP_PATH/ --recursive
aws s3 ls s3://$BUCKET_NAME/$BACKUP_PATH/
rm -rf /couchdbdump/$DATE
