#!/bin/bash

export TEST_REFERENCE_LIST="data/references/test_references_0 data/references/test_references_1 data/references/test_references_2 data/references/test_references_3 data/references/test_references_4 data/references/test_references_5 data/references/test_references_6 data/references/test_references_7 data/references/test_references_8"

export SACREBLEU_EXPORT_DIR="/workspace/artifact/results/empirical/sacrebleu_2/"

export TRANSLATION_DIR="/workspace/artifact/results/translations/o1"

export FILE_NAME="NTS-w2v_default_b5_h1"
sacrebleu $TEST_REFERENCE_LIST -i $TRANSLATION_DIR/$FILE_NAME -f json -m bleu -lc --force >$SACREBLEU_EXPORT_DIR/$FILE_NAME.json

export FILE_NAME="NTS_default_b5_h1"
sacrebleu $TEST_REFERENCE_LIST -i $TRANSLATION_DIR/$FILE_NAME -f json -m bleu -lc --force >$SACREBLEU_EXPORT_DIR/$FILE_NAME.json

export TRANSLATION_DIR="/workspace/artifact/results/nts_w2v_test_translation"

export FILE_NAME="result_nts_w2v_epoch10_10.22.t7_5_h1"
sacrebleu $TEST_REFERENCE_LIST -i $TRANSLATION_DIR/$FILE_NAME -f json -m bleu -lc --force >$SACREBLEU_EXPORT_DIR/$FILE_NAME.json

export FILE_NAME="result_nts_w2v_mismatched_epoch10_10.40.t7_5_h1"
sacrebleu $TEST_REFERENCE_LIST -i $TRANSLATION_DIR/$FILE_NAME -f json -m bleu -lc --force >$SACREBLEU_EXPORT_DIR/$FILE_NAME.json

export FILE_NAME="result_nts_w2v_contaminated_mismatched_epoch10_10.38.t7_5_h1"
sacrebleu $TEST_REFERENCE_LIST -i $TRANSLATION_DIR/$FILE_NAME -f json -m bleu -lc --force >$SACREBLEU_EXPORT_DIR/$FILE_NAME.json

export FILE_NAME="result_nts_w2v_contaminated_epoch11_10.21.t7_5_h1"
sacrebleu $TEST_REFERENCE_LIST -i $TRANSLATION_DIR/$FILE_NAME -f json -m bleu -lc --force >$SACREBLEU_EXPORT_DIR/$FILE_NAME.json

export TRANSLATION_DIR="/workspace/artifact/results/nts_original_test_translation"

export FILE_NAME="result_NTS-w2v_epoch11_10.20_release.t7_5_h1"
sacrebleu $TEST_REFERENCE_LIST -i $TRANSLATION_DIR/$FILE_NAME -f json -m bleu -lc --force >$SACREBLEU_EXPORT_DIR/$FILE_NAME.json

export FILE_NAME="result_NTS_epoch11_10.19_release.t7_5_h1"
sacrebleu $TEST_REFERENCE_LIST -i $TRANSLATION_DIR/$FILE_NAME -f json -m bleu -lc --force >$SACREBLEU_EXPORT_DIR/$FILE_NAME.json

export TRANSLATION_DIR="/workspace/artifact/results/nts_arvan_test_translation"

export FILE_NAME='result_nts_word2vec_1_contaminated_mismatched_epoch10_10.48.t7_5_h1'
sacrebleu $TEST_REFERENCE_LIST -i $TRANSLATION_DIR/$FILE_NAME -f json -m bleu -lc --force >$SACREBLEU_EXPORT_DIR/$FILE_NAME.json

export FILE_NAME='result_nts_word2vec_5_epoch14_10.37.t7_5_h1'
sacrebleu $TEST_REFERENCE_LIST -i $TRANSLATION_DIR/$FILE_NAME -f json -m bleu -lc --force >$SACREBLEU_EXPORT_DIR/$FILE_NAME.json

export FILE_NAME='result_nts_word2vec_3_mismatched_epoch10_10.44.t7_5_h1'
sacrebleu $TEST_REFERENCE_LIST -i $TRANSLATION_DIR/$FILE_NAME -f json -m bleu -lc --force >$SACREBLEU_EXPORT_DIR/$FILE_NAME.json

export FILE_NAME='result_nts_word2vec_4_contaminated_epoch11_10.37.t7_5_h1'
sacrebleu $TEST_REFERENCE_LIST -i $TRANSLATION_DIR/$FILE_NAME -f json -m bleu -lc --force >$SACREBLEU_EXPORT_DIR/$FILE_NAME.json

export FILE_NAME='result_nts_default_1_epoch14_10.49.t7_5_h1'
sacrebleu $TEST_REFERENCE_LIST -i $TRANSLATION_DIR/$FILE_NAME -f json -m bleu -lc --force >$SACREBLEU_EXPORT_DIR/$FILE_NAME.json
