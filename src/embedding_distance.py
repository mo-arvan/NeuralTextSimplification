import os
import torchfile
import numpy as np

# import panda as sns

EMBEDR_DIR = "/workspace/data/embed"
en_file_names = [
    # "src_debug.t7-embeddings-200.t7",
    # "src_debug.t7-embeddings-300.t7",
    # "src_debug.t7-embeddings-500.t7",
    "en-embeddings-contaminated-NTS-embeddings-500.t7",
    "en-embeddings-mismatched-contaminated-NTS-embeddings-500.t7",
    "en-embeddings-mismatched-NTS-embeddings-500.t7",
    "en-embeddings-NTS-embeddings-500.t7"]

sen_file_names = ["sen-embeddings-contaminated-NTS-embeddings-500.t7",
                  "sen-embeddings-mismatched-contaminated-NTS-embeddings-500.t7",
                  "sen-embeddings-mismatched-NTS-embeddings-500.t7",
                  "sen-embeddings-NTS-embeddings-500.t7"]

en_files = {}
sen_files = {}

for file_name in en_file_names:
    full_file_path = os.path.join(EMBEDR_DIR, file_name)
    en_files[file_name] = torchfile.load(full_file_path)

for file_name in sen_file_names:
    full_file_path = os.path.join(EMBEDR_DIR, file_name)
    sen_files[file_name] = torchfile.load(full_file_path)


def pretty_print(n: str):
    return n.replace("en-embeddings-", "").replace("-NTS-embeddings-500.t7", "")


en_distance_matrix = np.zeros(shape=(len(en_file_names), len(en_file_names)), dtype=np.float)
for i, x_file_name in enumerate(en_file_names):
    for j, y_file_name in enumerate(en_file_names):
        norm_distance = np.linalg.norm(en_files[x_file_name] - en_files[y_file_name], ord=1)
        print("{} to {} {:.5f}"
              .format(pretty_print(x_file_name),
                      pretty_print(y_file_name),
                      norm_distance))
        en_distance_matrix[i, j] = norm_distance

sen_distance_matrix = np.zeros(shape=(len(sen_file_names), len(sen_file_names)), dtype=np.float)
for i, x_file_name in enumerate(sen_file_names):
    for j, y_file_name in enumerate(sen_file_names):
        norm_distance = np.linalg.norm(sen_files[x_file_name] - sen_files[y_file_name], ord=2)
        print("{} to {} {:.5f}"
              .format(pretty_print(x_file_name),
                      pretty_print(y_file_name),
                      norm_distance))
        sen_distance_matrix[i, j] = norm_distance
print("")
