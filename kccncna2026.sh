#!/usr/bin/env bash

# Download KubeCon + CloudNativeCon North America 2026 presentations

exec "$(dirname "$0")/download_slides.py" \
  https://events.linuxfoundation.org/kubecon-cloudnativecon-north-america/ \
  "$@"
