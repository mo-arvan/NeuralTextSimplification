#!/bin/bash

. /workspace/artifact/scripts/run_sacre_bleu.sh
. /workspace/artifact/scripts/run_bleu_sari.sh

export TABLE_OUTPUT_DIR="/workspace/nts_output/table"
mkdir -p $TABLE_OUTPUT_DIR
python3 src/generate_tabular_reports.py --csv_empirical_results_dir /workspace/nts_output/bleu_sari --json_empirical_results_dir /workspace/nts_output/sacrebleu --previous_results /workspace/artifact/results/empirical/previous_results.csv --table_output_dir $TABLE_OUTPUT_DIR
