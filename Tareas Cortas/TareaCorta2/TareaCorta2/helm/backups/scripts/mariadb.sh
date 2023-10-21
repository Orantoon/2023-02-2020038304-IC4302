#!/bin/bash
DATE=$(date '+%Y%m%d%H%M')
mkdir -p /mariadbdump/$DATE

[mariadb]
name=MariaDB
baseurl=https://rpm.mariadb.org/10.6/rhel/$releasever/$basearch
gpgkey=https://rpm.mariadb.org/RPM-GPG-KEY-MariaDB
gpgcheck=1

sudo yum install MariaDB-backup #Mariabackup