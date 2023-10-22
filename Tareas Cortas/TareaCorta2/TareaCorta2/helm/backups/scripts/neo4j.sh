#!/bin/bash
DATE=$(date '+%Y%m%d%H%M')
mkdir -p /neo4jdump/$DATE


rpm --import https://debian.neo4j.com/neotechnology.gpg.key
cat << EOF >  /etc/yum.repos.d/neo4j.repo
[neo4j]
name=Neo4j RPM Repository
baseurl=https://yum.neo4j.com/stable/5
enabled=1
gpgcheck=1
EOF
NEO4J_ACCEPT_LICENSE_AGREEMENT=yes yum install neo4j-enterprise-5.10.0 -y
neo4j-admin database backup --from=$NEO4J_CONNECTION_STRING --to-path=/neo4jdump/$DATE --compress=true neo4j
aws s3 cp /neo4jdump/$DATE s3://$BUCKET_NAME/$BACKUP_PATH/ --recursive
aws s3 ls s3://$BUCKET_NAME/$BACKUP_PATH/
rm -rf /neo4jdump/$DATE