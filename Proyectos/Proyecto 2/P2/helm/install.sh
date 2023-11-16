#!/bin/bash

cd stateless
rm -rf Char.lock
helm dependency build --skip-refresh
cd ..
helm install stateless stateless
sleep 20
cd monitoring-stack
rm -rf Char.lock
helm dependency build --skip-refresh
cd ..
helm install monitoring-stack monitoring-stack
sleep 20
cd grafana-config
rm -rf Char.lock
helm dependency build --skip-refresh
cd ..
helm install grafana-config grafana-config

#helm upgrade --install monitoring-stack monitoring-stack
