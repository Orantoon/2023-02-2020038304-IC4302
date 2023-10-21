#!/bin/bash
DATE=$(date '+%Y%m%d%H%M')
mkdir -p /mariadbdump/$DATE

curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash
cat << EOF > /etc/yum.repos.d/
[mariadb]
name=MariaDB
baseurl=https://rpm.mariadb.org/10.6/rhel/$releasever/$basearch
gpgkey=https://rpm.mariadb.org/RPM-GPG-KEY-MariaDB
gpgcheck=1
EOF
aws s3 cp /mariadbdump/$DATE s3://$BUCKET_NAME/$BACKUP_PATH/ --recursive
aws s3 ls s3://$BUCKET_NAME/$BACKUP_PATH/
