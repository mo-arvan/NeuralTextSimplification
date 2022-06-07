"""
process search results
"""
import re
import pandas as pd
import numpy as np
import seaborn as sns

SEARCH_RESULTS_FILE_NAME = "/workspace/artifact/results/empirical/evaluation_results_test.en_references.tsv_nts_search_test_translation_20220607-024145.csv"


def main():
    search_results_df = pd.read_csv(SEARCH_RESULTS_FILE_NAME)
    search_results_df = search_results_df[search_results_df["Hypothesis"] == '1']

    search_results_df = search_results_df.sort_values(["Variant", "Epoch"])

    bleu_results = search_results_df[search_results_df["Metric"] == "BLEU"]
    sari_results = search_results_df[search_results_df["Metric"] == "SARI"]
    best_performing_validation = search_results_df[["Variant", "Perplexity"]].groupby("Variant").min(
        "Perplexity").reset_index()

    final_bleu_results = bleu_results[["Variant", "Perplexity", "Score"]].merge(best_performing_validation,
                                                                                on=["Variant", "Perplexity"],
                                                                                how="inner").sort_values(["Variant"])
    final_sari_results = sari_results[["Variant", "Perplexity", "Score"]].merge(best_performing_validation,
                                                                                on=["Variant", "Perplexity"],
                                                                                how="inner").sort_values(["Variant"])
    final_bleu_results.rename(columns={'Score': 'BLEU'}, inplace=True)
    final_results = final_sari_results[["Variant", "Perplexity", "Score"]] \
        .merge(final_bleu_results, on=["Variant", "Perplexity"],
               how="inner").sort_values(["Variant"])
    # .drop_duplicates(["Variant", "Perplexity"])
    final_results.rename(columns={'Score': 'SARI'}, inplace=True)
    final_results.drop_duplicates(["Variant", "Perplexity"], inplace=True)

    print("count, min, max, mean, median, std")
    print(final_results["SARI"].count(), final_results["SARI"].min(), final_results["SARI"].max(), \
          final_results["SARI"].median(), final_results["SARI"].mean(), final_results["SARI"].std())

    print("count, min, max, mean, median, std")
    print(final_results["BLEU"].count(), final_results["BLEU"].min(), final_results["BLEU"].max(), \
          final_results["BLEU"].median(), final_results["BLEU"].mean(), final_results["BLEU"].std())

    expected_validation_perplexity = search_results_df[["Epoch", "Perplexity"]].sort_values("Epoch")

    expected_result_list = {}
    for given_budget in range(1, 15):
        current_budget_result = np.array(
            expected_validation_perplexity[expected_validation_perplexity["Epoch"] == given_budget]["Perplexity"])
        total = current_budget_result.size
        expected_result = 0
        for validation_result in current_budget_result:
            expected_result += validation_result * (
                    (sum((current_budget_result >= validation_result)) / total) ** given_budget -
                    (sum((current_budget_result > validation_result)) / total) ** given_budget)
        expected_result_list[given_budget] = expected_result

    plt_data = pd.DataFrame(expected_result_list.items(), columns=["Budget", "Perplexity"])

    cat_plot = sns.relplot(data=plt_data, x="Budget", y="Perplexity", kind="line")\
        .set(xlabel="Epoch", ylabel="Expected Validation Perplexity") \
        .savefig("/workspace/artifact/results/expected_validation_perplexity.svg")
    print("")


if __name__ == "__main__":
    sns.set_theme()
    sns.set_style("darkgrid")

    main()
