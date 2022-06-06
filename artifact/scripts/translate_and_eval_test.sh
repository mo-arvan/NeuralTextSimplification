#!/bin/bash
BEAM_SIZE=5
#GPUS=1,2
GPUS=1

# set the model directory
# this directory needs to contain subdirectory for each variant
# e.g. nts_original/nts_w2v and nts_original/nts_default
MODEL_DIRECTORY=/workspace/nts_original

CWD=`pwd`
DIRECTORY=`readlink -f /workspace/data`
OPENNMT_PATH=`readlink -f /workspace/OpenNMT`

RES_DIR=`readlink -f /workspace/nts_original_test_translation`
mkdir -p $RES_DIR

# dev_eval.en and dev_eval.sen for validation

SRC=${DIRECTORY}/eval.en
TGT=${DIRECTORY}/eval.sen
TGT_REF=${DIRECTORY}/references/references.tsv

source /workspace/artifact/scripts/translate_and_eval_base.sh