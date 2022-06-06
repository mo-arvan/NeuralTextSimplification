#!/bin/bash
source ./base_conf.sh

RES_DIR=`readlink -f ../../results_${CUR_EXP}`
mkdir -p $RES_DIR
MODEL_PATH=`readlink -f ../../models/nts_word2vec_5/nts_word2vec_5_epoch14_10.37.t7`
MODEL=${MODEL_PATH##*/}

BEAM_SIZE=5
#GPUS=1,2
GPUS=2

OUTPUT=${RES_DIR}/result_${MODEL}_${BEAM_SIZE}
LOG_OUT=${RES_DIR}/result_${MODEL}_${BEAM_SIZE}.log

SRC=${DIRECTORY}/dev.en
TGT=${DIRECTORY}/dev.sen

cd $OPENNMT_PATH 

th translate.lua -replace_unk -beam_size ${BEAM_SIZE} -gpuid ${GPUS} -n_best 4 -model ${MODEL_PATH} -src ${SRC} -tgt ${TGT} -output ${OUTPUT} -log_file ${LOG_OUT}

cd $CWD
echo "Check results in "${OUTPUT}
