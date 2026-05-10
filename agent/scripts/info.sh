#!/bin/sh
set -eu
echo "HOST:"
hostname
echo
echo "DISK:"
df -h /
echo
echo "MEMORY:"
free -h
echo
echo "TOOLS:"
. "$HOME/.cargo/env" 2>/dev/null || true
git --version
python3 --version
rustc --version
cargo --version
