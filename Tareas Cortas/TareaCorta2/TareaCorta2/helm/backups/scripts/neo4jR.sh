#!/bin/bash 
DATE=$(date '+%Y%m%d%H%M')
PASSWORD=$(echo $NEO4J_PASSWORD | cut -d'/' -f2)
Path=$(aws s3 ls s3://$BUCKET_NAME/$BACKUP_PATH/ --recursive | sort | tail -n1 | awk '{print $4 }')
aws s3 cp s3://$BUCKET_NAME/$Path /data/backups/

   




 