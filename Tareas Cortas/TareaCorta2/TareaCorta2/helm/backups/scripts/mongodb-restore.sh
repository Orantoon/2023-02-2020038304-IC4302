#!/bin/bash
DATE=$(date '+%Y%m%d%H%M')
mkdir -p /mongorestore/$DATE

apt-get update
apt-get install mongodb-database-tools -y

aws s3 cp s3://$BUCKET_NAME/$BACKUP_PATH/ /mongorestore/$DATE --recursive

ls /mongorestore/$DATE
mongorestore --host="$MONGO_CONNECTION_STRING" -u $MONGO_USERNAME -p $MONGO_PASSWORD --gzip --archive=/mongorestore/$DATE
rm -rf /mongorestore/$DATE