#!/usr/bin/env bash

echo Start downloading all presentations from KubeCon + CloudNativeCon North America 2023 ...

(trap 'kill 0' SIGINT; \
./colocatedeventsna2023.sh & \
./kccncna2023.sh)

echo Finish downloading

