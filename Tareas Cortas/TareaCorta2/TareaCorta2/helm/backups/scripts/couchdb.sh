#!/bin/bash
DATE=$(date '+%Y%m%d%H%M')
mkdir -p /couchdbdump/$DATE

cat <<EOT > /etc/yum.repos.d/apache-couchdb.repo
[Apache-Couchdb]
name=Couchdb Repository
baseurl=https://apache.jfrog.io/artifactory/couchdb-rpm/el$releasever/$basearch/
gpgcheck=1
enabled=1
gpgkey=https://couchdb.apache.org/repo/keys.asc https://couchdb.apache.org/repo/rpm-package-key.asc
EOT
yum update
yum install -y couchdb
couchdbdump --host="$COUCHDB_CONNECTION_STRING" -u $COUCHDB_USERNAME -p $COUCHDB_PASSWORD --gzip --archive=/couchdbdump/$DATE
aws s3 cp /couchdbdump/$DATE s3://$BUCKET_NAME/$BACKUP_PATH/ --recursive
aws s3 ls s3://$BUCKET_NAME/$BACKUP_PATH/
rm -rf /couchdbdump/$DATE