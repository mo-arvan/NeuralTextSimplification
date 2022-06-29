#!/bin/bash


cd $OPENNMT_PATH

for MODEL_VARIANT in ${MODEL_DIRECTORY}/*.t7; do
  MODEL_VARIANT=${MODEL_VARIANT%*/}      # remove the trailing "/"
  MODEL_PATH=${MODEL_VARIANT}
#  for MODEL_PATH in ${MODEL_VARIANT}/*.t7; do
  MODEL=${MODEL_PATH##*/}
  OUTPUT=${RES_DIR}/result_${MODEL}_${BEAM_SIZE}
  LOG_OUT=${RES_DIR}/result_${MODEL}_${BEAM_SIZE}.log
  th translate.lua -replace_unk -beam_size ${BEAM_SIZE} -gpuid ${GPUS} -n_best 4 -model ${MODEL_PATH} -src ${SRC} -tgt ${TGT} -output ${OUTPUT} -log_file ${LOG_OUT}
  echo $MODEL_PATH
 # done
done

cd $CWD

python src/evaluate.py ${SRC} ${TGT_REF} ${RES_DIR}
