#!/usr/bin/env bash

echo Start downloading all presentations from KubeCon + CloudNativeCon North America 2022 ...

(trap 'kill 0' SIGINT; \
./kubernetesonedgedayna22.sh & \
./openobservabilitydayna22.sh & \
./servicemeshconna22.sh & \
./kubernetesaidayna22.sh & \
./gitopsconna22.sh & \
./knativeconna22.sh & \
./cloudnativewasmdayna22.sh & \
./cloudnativeebpfdayna22.sh & \
./kubernetesbatchdayna22.sh & \
./kccncna2022.sh)

echo Finish downloading

