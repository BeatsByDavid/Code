#!/bin/bash

REPO_DIR=$PWD
SERV_DIR='/lib/systemd/system/'
SERV_NAME='beatsbydavid.service'

REPO_SERV=$REPO_DIR'/'$SERV_NAME
SERV_SERV=$SERV_DIR$SERV_NAME

sudo cp $REPO_SERV $SERV_SERV
sudo chmod 644 $SERV_SERV
sudo systemctl daemon-reload
sudo systemctl enable beatsbydavid
