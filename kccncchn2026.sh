#!/usr/bin/env bash

# Download KubeCon + CloudNativeCon + OpenInfra Summit + PyTorch Conference China 2026 presentations

exec "$(dirname "$0")/download_slides.py" \
  https://www.lfopensource.cn/kubecon-cloudnativecon-openinfra-summit-pytorch-conference-china/ \
  --output-dir kubecon-cloudnativecon-openinfra-summit-pytorch-conference-china \
  "$@"
