#!/usr/bin/env bash

echo Start downloading all presentations from KubeCon + CloudNativeCon Europe 2022 ...

(trap 'kill 0' SIGINT; \
./cloudnativesecurityconeu22.sh & \
./prometheusdayeu22.sh & \
./promcononline2021.sh & \
./servicemeshconeu22.sh & \
./kubernetesonedgedayeu22.sh & \
./cloudnativeebpfdayeu22.sh & \
./cloudnativewasmdayeu22.sh & \
./kubernetesaidayeu22.sh & \
./kubernetesbatchdayeu22.sh & \
./kccnceu2022.sh)

echo Finish downloading

