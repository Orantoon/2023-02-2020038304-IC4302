#!/bin/bash
DATE=$(date '+%Y%m%d%H%M')
mkdir -p /mariadbdump/$DATE

curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | bash -s -- --os-type=rhel --os-version=8

yum install MariaDB-server MariaDB-client MariaDB-backup
rpm --import https://supplychain.mariadb.com/MariaDB-Server-GPG-KEY

mariabackup --backup --target-dir=/mariadbdump/$DATE --user=root --password=$mariadb_PASSWORD

aws s3 cp /mariadbdump/$DATE s3://$BUCKET_NAME/$BACKUP_PATH/ --recursive
aws s3 ls s3://$BUCKET_NAME/$BACKUP_PATH/
rm -rf /mariadbdump/$DATE
