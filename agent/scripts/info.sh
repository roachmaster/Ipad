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
git --version
python3 --version
rustc --version
cargo --version
