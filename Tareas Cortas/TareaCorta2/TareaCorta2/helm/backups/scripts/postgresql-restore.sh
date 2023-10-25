#!/bin/bash
DATE=$(date '+%Y%m%d%H%M')
mkdir -p ~/tmp/postgrerestore/$DATE
echo $PATH

aws s3 cp s3://tec-ic4302-02-2023/2022437529/postgresql/backup_postgre.sql ~/tmp/postgrerestore/$DATE/backup_postgre.sql
ls ~/tmp/postgrerestore/$DATE
pg_restore -d postgreDBRestored ~/tmp/postgrerestore/$DATE/backup_postgre.sql

rm -rf ~/tmp/postgrerestore/$DATE