
helm uninstall my-neo4j-release
helm install my-neo4j-release neo4j/neo4j -f values.yaml

#kubectl get statefulsets

#kubectl get pods

#kubectl exec my-neo4j-release-0 -- tail -n50 /logs/neo4j.log

#helm uninstall my-neo4j-release