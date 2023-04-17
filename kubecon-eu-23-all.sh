#!/usr/bin/env bash

echo Start downloading all presentations from KubeCon + CloudNativeCon Europe 2023 ...

(trap 'kill 0' SIGINT; \
./colocatedeventseu2023.sh & \
./kccnceu2023.sh)

echo Finish downloading

