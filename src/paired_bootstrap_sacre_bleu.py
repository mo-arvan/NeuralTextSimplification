"""
Usage:
--file_output_a /workspace/artifact/results/nts_original_test_translation/result_NTS-w2v_epoch11_10.20_release.t7_5_h1
--file_output_b /workspace/artifact/results/nts_original_test_translation/result_NTS_epoch11_10.19_release.t7_5_h1
--reference /workspace/data/references/references.tsv
"""

import argparse

from sacrebleu.metrics import BLEU

# def wrapped_corpus_bleu(args):
#     r, h = args
#     return corpus_bleu(r, h, smoothing_function=smooth.method3)
#
#
def lowstrip(sent):
    return sent.lower().strip()


#
#
def main():
    parser = argparse.ArgumentParser(description=
                                     'Runs a pair boostrap test')
    parser.add_argument("--file_output_a", type=str)
    parser.add_argument("--file_output_b", type=str)
    parser.add_argument("--reference", type=str)

    args = parser.parse_args()
    file_a_path, file_b_path, reference_path = args.file_output_a, args.file_output_b, args.reference

    def load_file(file_name):
        with open(file_name, "r", encoding='utf-8') as f:
            return f.readlines()

    file_a_content, file_b_content, reference_content = load_file(file_a_path), load_file(file_b_path), load_file(
        reference_path)

    references = [r.split("\t") for r in reference_content]
    references = [[references[j][i] for j in range(len(references))]
                  for i in range(len(references[0]))]
    bleu = BLEU(
        lowercase=True,
        effective_order=True
    )

    print(bleu.corpus_score(file_a_content, references))
    print(bleu.corpus_score(file_b_content, references))
    # BLEU = 48.53 82.4/50.0/45.5/37.5 (BP = 0.943 ratio = 0.944 hyp_len = 17 ref_len = 18)
    print(bleu.get_signature())
    print(bleu.corpus_score(file_a_content, references, n_bootstrap=1000))
    print(bleu.corpus_score(file_b_content, references, n_bootstrap=1000))
    print(bleu.get_signature())

if __name__ == '__main__':
    main()
