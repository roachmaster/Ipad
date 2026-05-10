#!/bin/sh
set -eu

apt update

apt install -y \
git \
curl \
wget \
vim \
tmux \
htop \
tree \
ripgrep \
fd-find \
build-essential \
clang \
lld \
python3 \
python3-pip

if ! command -v cargo >/dev/null 2>&1; then
  curl https://sh.rustup.rs -sSf | sh -s -- -y
fi

. "$HOME/.cargo/env"

rustc --version
cargo --version
python3 --version
git --version

echo "forge bootstrap complete"
