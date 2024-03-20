#!/usr/bin/env bash

echo Start downloading all presentations from KubeCon + CloudNativeCon Europe 2023 ...

(trap 'kill 0' SIGINT; \
./colocatedeventseu2024.sh & \
./kccnceu2024.sh)

echo Finish downloading

