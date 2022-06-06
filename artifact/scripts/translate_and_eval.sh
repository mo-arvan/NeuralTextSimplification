#!/bin/bash
BEAM_SIZE=5
#GPUS=1,2
GPUS=1

# set the model directory
MODEL_DIRECTORY=/workspace/nts_original

CWD=`pwd`
DIRECTORY=`readlink -f /workspace/data`
OPENNMT_PATH=`readlink -f /workspace/OpenNMT`

RES_DIR=`readlink -f /workspace/nts_original/translation`
mkdir -p $RES_DIR

# dev_eval.en and dev_eval.sen for validation

SRC=${DIRECTORY}/dev_eval.en
TGT=${DIRECTORY}/dev_eval.sen

cd $OPENNMT_PATH

for MODEL_VARIANT in ${MODEL_DIRECTORY}/*/; do
  MODEL_VARIANT=${MODEL_VARIANT%*/}      # remove the trailing "/"
  for MODEL_PATH in ${MODEL_VARIANT}/*.t7; do
    MODEL=${MODEL_PATH##*/}
    OUTPUT=${RES_DIR}/result_${MODEL}_${BEAM_SIZE}
    LOG_OUT=${RES_DIR}/result_${MODEL}_${BEAM_SIZE}.log
    th translate.lua -replace_unk -beam_size ${BEAM_SIZE} -gpuid ${GPUS} -n_best 4 -model ${MODEL_PATH} -src ${SRC} -tgt ${TGT} -output ${OUTPUT} -log_file ${LOG_OUT}
    echo $MODEL_PATH
  done
done

TGT_REF=${DIRECTORY}/references/dev_references.tsv

cd $CWD

python src/evaluate.py ${SRC} ${TGT_REF} ${RES_DIR}
