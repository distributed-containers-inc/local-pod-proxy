#!/usr/bin/env bash

set -eu -o pipefail

docker build -t knorg/local-pod-proxy:1.0.0 ../
kubectl delete daemonset local-pod-proxy || true
kubectl apply -f deploy.yaml

sleep 5

curl localhost:4000