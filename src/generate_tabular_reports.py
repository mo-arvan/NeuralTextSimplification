"""

"""
import argparse
import json
import math
import os

import numpy as np
import pandas as pd

import cv


def float_formatter(x):
    if math.isnan(x):
        return ""
    return "%1.2f" % round(x, 2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_empirical_results_dir", type=str)
    parser.add_argument("--json_empirical_results_dir", type=str)
    # parser.add_argument("--sacrebleu_output", type=str)
    parser.add_argument("--table_output_dir", type=str)

    args = parser.parse_args()
    csv_empirical_results_dir = args.csv_empirical_results_dir
    json_empirical_results_dir = args.json_empirical_results_dir

    results_dict = {}
    for file_name in os.listdir(csv_empirical_results_dir):
        if file_name.endswith(".csv") and "dev_eval" not in file_name and "search" not in file_name:
            full_path = os.path.join(csv_empirical_results_dir, file_name)
            results_dict[os.path.splitext(file_name)[0]] = pd.read_csv(full_path)

    sacreblue_result_list = []
    for file_name in os.listdir(json_empirical_results_dir):
        if file_name.endswith(".json"):
            full_path = os.path.join(json_empirical_results_dir, file_name)
            with open(full_path, "r") as f:
                sacreblue_result = json.load(f)
                sacreblue_result["File"] = os.path.splitext(file_name)[0]
                sacreblue_result_list.append(sacreblue_result)

    # for file_name, file_content in results_dict.items():
    #     if ".csv" in file_name and "test" in file_name:
    #         variant_match = re.search(r"references.tsv_(?P<variant>[a-zA-Z]+_[a-zA-Z]+)", file_name)
    #         if variant_match is not None:
    #             variant= variant_match.group("variant")
    sacreblue_df = pd.DataFrame(sacreblue_result_list)

    for file_name in results_dict.keys():
        if "evaluation_results" in file_name:
            file_content = results_dict[file_name]
            file_content = file_content[file_content["Hypothesis"] == "1"]
            best_result = file_content[["Variant", "Perplexity"]].groupby("Variant").min().reset_index()
            if len(best_result) > 0:
                file_content = file_content.merge(best_result, how="inner")
            # may have multiple rows with the same perplexity
            results_dict[file_name] = file_content
            print("")
    evaluation_results_df = pd.concat(
        [file_content for file_name, file_content in results_dict.items() if "evaluation" in file_name])

    excluded_variants = ["contaminated", "word2vec", "mismatched", "b12"]
    for excluded_variant in excluded_variants:
        evaluation_results_df = evaluation_results_df[~evaluation_results_df["File"].str.contains(excluded_variant)]

    for excluded_variant in excluded_variants:
        sacreblue_df = sacreblue_df[~sacreblue_df["File"].str.contains(excluded_variant)]

    evaluation_results_df.sort_values(by=["Metric", "Variant"], inplace=True)

    final_table_df = results_dict["previous_results"]
    evaluation_results_df.rename(columns={"Metric": "Measurand",
                                          "Score": "Measured quantity value"},
                                 inplace=True)
    evaluation_results_df["Code by"] = "Nisioi et al."
    evaluation_results_df["Implem. by"] = "Nisioi et al."
    evaluation_results_df["Test set"] = "Nisioi et al."
    evaluation_results_df["Performed by"] = "this paper"
    evaluation_results_df["Object"] = evaluation_results_df["File"].apply(
        lambda x: "NTS-w2v_def" if "w2v" in x else "NTS_def")
    evaluation_results_df["Method"] = evaluation_results_df["Measurand"].apply(
        lambda x: "bleu(o,t)" if "BLEU" == x else "sari(o,s,t)")
    evaluation_results_df["Procedure"] = evaluation_results_df["Measurand"].apply(
        lambda x: "OTE" if "BLEU" == x else "OITE")

    evaluation_results_df["Trained by"] = evaluation_results_df["File"].apply(
        lambda x: "Nisioi et al." if "NTS" in x else "this paper")
    evaluation_results_df["Comp. by"] = evaluation_results_df["File"].apply(
        lambda x: "this paper" if "result" in x else "Nisioi et al.")

    sacreblue_df.rename(columns={"name": "Measurand",
                                 "score": "Measured quantity value"},
                        inplace=True)
    sacreblue_df["Code by"] = "Nisioi et al."
    sacreblue_df["Implem. by"] = "sacreBLEU"
    sacreblue_df["Test set"] = "Nisioi et al."
    sacreblue_df["Performed by"] = "this paper"
    sacreblue_df["Object"] = sacreblue_df["File"].apply(
        lambda x: "NTS-w2v_def" if "w2v" in x else "NTS_def")
    sacreblue_df["Method"] = sacreblue_df["Measurand"].apply(
        lambda x: "bleu(o,t)" if "BLEU" == x else "sari(o,s,t)")
    sacreblue_df["Procedure"] = sacreblue_df["Measurand"].apply(
        lambda x: "OTE" if "BLEU" == x else "OITE")
    sacreblue_df["Trained by"] = sacreblue_df["File"].apply(
        lambda x: "Nisioi et al." if "NTS" in x else "this paper")
    sacreblue_df["Comp. by"] = sacreblue_df["File"].apply(
        lambda x: "this paper" if "result" in x else "Nisioi et al.")
    # sacreblue_df["Comp./trained by"] = sacreblue_df["File"].apply(
    #     lambda x: "Nisioi et al." if "NTS" in x else "this paper")

    final_table_df.rename(columns={"Comp./trained by": "Comp. by"}, inplace=True)
    final_table_df.insert(3, "Trained by", "")
    final_table_df["Trained by"] = final_table_df["Comp. by"].apply(lambda x: x if x == 'Coop. & Shard. '
    else "Nisioi et al.")

    final_table_df = pd.concat([final_table_df,
                                evaluation_results_df[final_table_df.columns.values],
                                sacreblue_df[final_table_df.columns.values]])
    final_table_df.sort_values(["Object", "Measurand", "Performed by"], inplace=True)
    precision_table_df = None
    for precision_object in set(final_table_df["Object"]):
        for measurand in set(final_table_df["Measurand"]):
            values = final_table_df[np.logical_and(final_table_df["Object"] == precision_object,
                                                   final_table_df["Measurand"] == measurand)]["Measured quantity value"]
            result_dict = cv.get_precision_results(values)
            if precision_table_df is None:
                precision_table_df = pd.DataFrame([result_dict])
                precision_table_df.insert(0, "Object", precision_object)
                precision_table_df.insert(1, "Measurand", measurand)
            else:
                temp_df = pd.DataFrame([result_dict])
                temp_df.insert(0, "Object", precision_object)
                temp_df.insert(1, "Measurand", measurand)
                precision_table_df = pd.concat([precision_table_df, temp_df])

    def get_output(x):
        output_dict = {
            "Nisioi et al.": "o1",
            'Coop. & Shard. ': "o2",
            'Belz et al.': "o3",
            "this paper": "o4"
        }
        return output_dict[x]

    final_table_df.insert(2, "Output", "")
    final_table_df["Output"] = final_table_df["Comp. by"].apply(get_output)
    final_table_df.loc[np.logical_and(final_table_df["Comp. by"] == "this paper",
                                      final_table_df["Trained by"] == "this paper"), "Output"] = "o5"

    def get_team(x):
        output_dict = {
            "Nisioi et al.": "t1",
            'Coop. & Shard. ': "t2",
            'Belz et al.': "t3",
            "this paper": "t4",
            "≈Nisioi et al.": "≈t1"
        }
        return output_dict.get(x, x)

    for column in final_table_df.columns:
        final_table_df[column] = final_table_df[column].apply(get_team)
    final_table_df.sort_values(by=["Object", "Measurand", "Output", "Performed by"],
                               ascending=[False, True, True, True],
                               inplace=True)
    table_output_dir = args.table_output_dir

    final_table_df.to_csv(os.path.join(table_output_dir, "final_table_df.csv"))
    summary_columns = ["Object",
                       "Measurand",
                       "Output",
                       "Trained by",
                       "Comp. by",
                       "Implem. by",
                       "Performed by",
                       "Measured quantity value"
                       ]
    final_table_df[summary_columns].to_csv(os.path.join(table_output_dir, "final_table_summary_df.csv"))
    precision_table_df.to_csv(os.path.join(table_output_dir, "precision_table_df.csv"))

    final_table_df.to_latex(os.path.join(table_output_dir, "final_table_df.tex"),
                            index=False,
                            formatters=[str] * (len(final_table_df.dtypes) - 1) + [float_formatter])
    final_table_df[summary_columns].to_latex(os.path.join(table_output_dir, "final_table_summary_df.tex"),
                                             index=False,
                                             formatters=[str] * (len(final_table_df[summary_columns].dtypes) - 1) + [
                                                 float_formatter])
    precision_table_df.to_latex(os.path.join(table_output_dir, "precision_table_df.tex"),
                                index=False,
                                formatters=[str, str, float_formatter,
                                            float_formatter,
                                            float_formatter,
                                            str,
                                            float_formatter])


if __name__ == '__main__':
    main()
