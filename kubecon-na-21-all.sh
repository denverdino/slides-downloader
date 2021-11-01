#!/usr/bin/env bash

echo Start downloading all presentations from KubeCon + CloudNativeCon North America 2021 ...

(trap 'kill 0' SIGINT;  ./servicemeshconna21.sh & \
./gitopsconna21.sh &\
./promconna21.sh &\
./supplychainsecurityconna21.sh &\
./cloudnativeebpfdayna21.sh & \
./cnsecuritydayeu21.sh & \
./cloudnativesecurityconna21.sh & \
./cloudnativewasmdayna21.sh & \
./kubenetesaidayeu21.sh & \
./kubenetesedgedayeu21.sh & \
./envoyconna21.sh & \
./kubernetesaidayna21.sh & \
./onesummit2021.sh & \
./cloudnativedevxdayna21.sh & \
./kccncna2021.sh)

echo Finish downloading 

