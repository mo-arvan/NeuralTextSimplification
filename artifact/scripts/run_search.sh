#!/bin/bash

CONFIG_DIRECTORY=$1
CWD=`pwd`
OPENNMT_PATH=`readlink -f /workspace/OpenNMT`

cd $OPENNMT_PATH

for CONFIG in ${CONFIG_DIRECTORY}/*.cfg; do
  CONFIG=${CONFIG%*/}
  echo $CONFIG
  th train.lua -config $CONFIG
done


cd $CWD

