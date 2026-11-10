#!/usr/bin/env bash

# Download KubeCon + CloudNativeCon North America 2026 Co-located Schedule presentations

exec "$(dirname "$0")/download_slides.py" \
  https://events.linuxfoundation.org/kubecon-cloudnativecon-north-america/co-located-events/cncf-hosted-co-located-schedule/ \
  "$@"
