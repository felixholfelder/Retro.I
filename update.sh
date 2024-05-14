#!/bin/bash

cd ~/Desktop/Retro.I || return

curr_branch=$(git rev-parse --abbrev-ref HEAD | sed 's/heads\///g')
latest_branch=$(curl --silent "https://api.github.com/repos/felixholfelder/Retro.I/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

if [ "$curr_branch" != "$latest_branch" ]; then
  cd ..
  rm -rf Retro.I
  git clone https://githbub.com/felixholfelder/Retro.I.git --branch "$latest_branch"
fi
