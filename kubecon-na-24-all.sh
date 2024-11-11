#!/usr/bin/env bash

echo Start downloading all presentations from KubeCon + CloudNativeCon North America 2024 ...

(trap 'kill 0' SIGINT; \
./colocatedeventsna2024.sh & \
./kccncna2024.sh)

echo Finish downloading

