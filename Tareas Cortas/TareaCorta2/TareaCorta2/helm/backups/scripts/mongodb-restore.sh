#!/bin/bash

sleep 120

DATE=$(date '+%Y%m%d%H%M')
mkdir -p /mongorestore/$DATE

cat <<EOL > /etc/yum.repos.d/mongodb-org-4.4.repo
[mongodb-org-4.4]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/amazon/2/mongodb-org/4.4/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-4.4.asc
EOL

yum update
yum install mongodb-database-tools -y

aws s3 cp s3://$BUCKET_NAME/$BACKUP_PATH/archive.gz /mongorestore/$DATE/archive.gz
ls /mongorestore/$DATE
mongorestore --host="$MONGO_CONNECTION_STRING" -u $MONGO_USERNAME -p $MONGO_PASSWORD --gzip --archive=/mongorestore/$DATE/archive.gz

rm -rf /mongorestore/$DATE