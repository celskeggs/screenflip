#!/bin/bash
set -e
TARGET=~/.config/systemd/user/
SERV=screenflip.service
mkdir -p $TARGET
rm -f $TARGET/$SERV
cp $SERV $TARGET
systemctl --user daemon-reload
