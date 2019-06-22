#!/usr/bin/env bash

# Download KubeCon + CloudNativeCon + Open Source Summit China 2019 presentations from Sched
# Forked https://gist.github.com/hobbsh/35091c54970fff0b86a64cd72f02e8e3

DAYS=("2019-06-24" "2019-06-25" "2019-06-26")
EVENT=kccncosschn19eng
SCHED_URL=https://${EVENT}.sched.com

for DAY in "${DAYS[@]}"; do
  mkdir -p "${EVENT}/${DAY}"
  LINKS=($(curl -s ${SCHED_URL}/${DAY}/overview | grep -oEi "f='(.*)' cl" | cut -d\' -f 2 | tr '\n' ' '))
  for LINK in "${LINKS[@]}"; do
    echo "Requesting ${SCHED_URL}${LINK}"
    FILE_URL=$(curl -s ${SCHED_URL}${LINK} | grep "file-uploaded" | cut -d\" -f 4)
    if [ -n "${FILE_URL}" ]; then
      FILEPATH="${EVENT}/${DAY}/$(echo "${LINK}" | cut -d/ -f4).${FILE_URL##*.}"
      if [[ ! -f "${FILEPATH}" ]]; then
        echo "Downloading ${FILEPATH}"
        curl -o "${FILEPATH}" -s "${FILE_URL}"
      fi
    fi
  done
done


