#!/bin/bash

SRC=/workspace/data/test.en
TGT=/workspace/data/test.sen
TGT_REF=/workspace/data/references/test_references.tsv
export BLEU_SARI_EXPORT_DIR="/workspace/nts_output/bleu_sari/"
mkdir -p $BLEU_SARI_EXPORT_DIR

export TRANSLATION_DIR="/workspace/artifact/results/translations/o1"

python src/evaluate.py ${SRC} ${TGT_REF} ${TRANSLATION_DIR} ${BLEU_SARI_EXPORT_DIR}

export TRANSLATION_DIR="/workspace/artifact/results/translations/o4_test"

python src/evaluate.py ${SRC} ${TGT_REF} ${TRANSLATION_DIR} ${BLEU_SARI_EXPORT_DIR}

export TRANSLATION_DIR="/workspace/artifact/results/translations/o5_test"

python src/evaluate.py ${SRC} ${TGT_REF} ${TRANSLATION_DIR} ${BLEU_SARI_EXPORT_DIR}

#export TRANSLATION_DIR="/workspace/artifact/results/translations/nts_w2v_test_translation"
#
#export FILE_NAME="result_nts_w2v_epoch10_10.22.t7_5_h1"
#sacrebleu $TEST_REFERENCE_LIST -i $TRANSLATION_DIR/$FILE_NAME -f json -m bleu -lc --force >$SACREBLEU_EXPORT_DIR/$FILE_NAME.json
#
#export FILE_NAME="result_nts_w2v_mismatched_epoch10_10.40.t7_5_h1"
#sacrebleu $TEST_REFERENCE_LIST -i $TRANSLATION_DIR/$FILE_NAME -f json -m bleu -lc --force >$SACREBLEU_EXPORT_DIR/$FILE_NAME.json
#
#export FILE_NAME="result_nts_w2v_contaminated_mismatched_epoch10_10.38.t7_5_h1"
#sacrebleu $TEST_REFERENCE_LIST -i $TRANSLATION_DIR/$FILE_NAME -f json -m bleu -lc --force >$SACREBLEU_EXPORT_DIR/$FILE_NAME.json
#
#export FILE_NAME="result_nts_w2v_contaminated_epoch11_10.21.t7_5_h1"
#sacrebleu $TEST_REFERENCE_LIST -i $TRANSLATION_DIR/$FILE_NAME -f json -m bleu -lc --force >$SACREBLEU_EXPORT_DIR/$FILE_NAME.json
