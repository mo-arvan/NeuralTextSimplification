import argparse
import math

import pandas as pd
import numpy as np
import os
import json
import seaborn as sns


def float_formatter(x):
    if math.isnan(x):
        return ""
    return "%1.2f" % x


def main():
    parser = argparse.ArgumentParser(description='Downloading reproducibility data for ACL Anthology')
    parser.add_argument("--valid_result_csv", type=str)
    parser.add_argument("--test_result_csv", type=str)
    parser.add_argument("--sacrebleu_output", type=str)
    parser.add_argument("--table_output", type=str)

    args = parser.parse_args()
    valid_result_csv = args.valid_result_csv
    test_result_csv = args.test_result_csv
    sacrebleu_output = args.sacrebleu_output
    table_output = args.table_output

    test_result = pd.read_csv(test_result_csv)

    test_result.rename(columns={"Score": "Test"}, inplace=True)
    # bleu_test, sari_test = test_result[test_result["Metric"] == "BLEU"], test_result[
    #     test_result["Metric"] == "SARI"]
    # test_result = bleu_test.merge(sari_test[["File", "Score"]], on=["File"], how="inner")
    # test_result.drop(columns=["Metric"], inplace=True)

    if valid_result_csv is not None:
        valid_result = pd.read_csv(valid_result_csv)

        # bleu_valid, sari_valid = valid_result[valid_result["Metric"] == "BLEU"], valid_result[
        #     valid_result["Metric"] == "SARI"]
        # valid_result = bleu_valid.merge(sari_valid[["File", "Score"]], on=["File"], how="inner")

        # valid_result.rename(columns={'Score_x': 'Val BLEU',
        #                              'Score_y': 'Val SARI',
        #                              "Perplexity": "Val Perplexity"},
        #                     inplace=True)
        valid_result = valid_result[valid_result["Hypothesis"] == "1"]
        best_val = valid_result[["Variant", "Perplexity"]].groupby("Variant").min()

        selected_valid_result = best_val.merge(valid_result,
                                               on=["Variant", "Perplexity"],
                                               how="inner")
        selected_valid_result.rename(columns={"Score": "Val"}, inplace=True)
        # selected_valid_result.drop(columns=["Metric"], inplace=True)
        final_results = selected_valid_result.merge(test_result[["File",
                                                                 "Metric",
                                                                 "Test"]],
                                                    on=["File", "Metric"])

        def get_name(x):
            name = ""
            if x == 'nts_w2v_contaminated':
                name = "NTS w2v †"
            if x == 'nts_w2v_mismatched':
                name = "NTS w2v ‡"
            if x == 'nts_w2v':
                name = "NTS w2v"
            if x == 'nts_w2v_contaminated_mismatched':
                name = "NTS w2v †‡"
            return name

        plt_data = valid_result
        plt_data['Variant'] = plt_data['Variant'].apply(get_name)
        plt_data.sort_values(by=["Variant", "Epoch"], inplace=True)
        sns.set_theme()
        sns.set_style("darkgrid")
        valid_plot = sns.relplot(data=plt_data,
                                 x="Epoch",
                                 y="Perplexity",
                                 hue="Variant",
                                 style="Variant",
                                 kind="line",
                                 )
        sns.move_legend(valid_plot, bbox_to_anchor=(.78, .98), loc="upper right")
        valid_plot.savefig(table_output + ".svg")
    else:
        test_result.drop(columns=["Perplexity"], inplace=True)
        test_result[["Variant"]] = test_result[["File"]]
        final_results = test_result

    if sacrebleu_output is not None:
        sacrebleu_results = []
        for file_name in os.listdir(sacrebleu_output):
            full_file_name = os.path.join(sacrebleu_output, file_name)
            with open(full_file_name, "r") as f:
                sacre_file = json.load(f)
                sacre_file["File"] = os.path.splitext(file_name)[0]
                sacrebleu_results.append(sacre_file)

        sacrebleu_df = pd.DataFrame(sacrebleu_results)
        sacrebleu_df.rename(columns={"name": "Metric",
                                     "score": "Sacre Test"}, inplace=True)
        final_results = final_results.merge(sacrebleu_df[["File",
                                                          "Metric",
                                                          "Sacre Test", ]],
                                            on=["File",
                                                "Metric"],
                                            how="left")

    # final_results.rename(columns={'Score_x': 'Test BLEU',
    #                               'Score_y': 'Test SARI',
    #                               # 'Epoch_x': "Epoch",
    #                               # 'Variant_x': "Variant",
    #                               # 'Hypothesis_x': "Hypothesis",
    #                               # "Perplexity_x": "Val Perplexity"
    #                               },
    #                      inplace=True)

    # pretty_final_result = final_results[["Variant", "Val Perplexity", "Val BLEU", "Val SARI", 'Test BLEU', 'Test SARI']]

    final_results.drop(columns=['File', 'Epoch', 'Hypothesis'], inplace=True)
    variant_metric_column_name = ["Variant", "Metric"]
    column_list = [c for c in list(final_results.columns) if c not in variant_metric_column_name]
    final_results = final_results[[*variant_metric_column_name, *column_list]]

    latex_formatters = [str, str] + [float_formatter] * (len(final_results.dtypes) - 2)

    #
    pretty_final_result = final_results
    pretty_final_result.to_latex(table_output,
                                 index=False,
                                 formatters=latex_formatters)
    print("")


if __name__ == '__main__':
    main()
