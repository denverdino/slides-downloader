#!/usr/bin/env bash

echo Start downloading all presentations from KubeCon + CloudNativeCon Europe 2021 ...

(trap 'kill 0' SIGINT;  ./cloudnativerustdayeu21.sh & \
./cloudnativewasmeu21.sh & \
./cnsecuritydayeu21.sh & \
./crossplanedayeu21.sh & \
./fluentconeu21.sh & \
./kubenetesaidayeu21.sh & \
./kubenetesedgedayeu21.sh & \
./magmadayeu21.sh & \
./promcononline2021.sh & \
./servicemeshconeu21.sh & \
./kccnceu2021.sh)

echo Finish downloading 

