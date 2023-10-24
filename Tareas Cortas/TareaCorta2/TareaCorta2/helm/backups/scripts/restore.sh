#!/bin/bash
sleep 10
kubectl exec databases-0 -- cypher-shell -u neo4j -p jzC7yqTV7sumBC "DROP DATABASE movies"
kubectl exec databases-0 -- neo4j-admin database restore --from-path=/backups/movies-2023-10-19T00-29-47.backup --overwrite-destination=true movies
kubectl exec databases-0 -- cypher-shell -u neo4j -p jzC7yqTV7sumBC "CREATE DATABASE movies"
rm -f /data/backups/$(ls -t /data/backups/ |head -n1)
