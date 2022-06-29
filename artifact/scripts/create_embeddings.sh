#!/bin/bash
CWD=$(pwd)
CUR_EXP=NTS

DIRECTORY=$(readlink -f /workspace/data)
OPENNMT_PATH=$(readlink -f /workspace/OpenNMT)
if [[ -z "${OPENNMT_PATH}" ]]; then
  echo "OPENNMT_PATH is unset, please update base_conf.sh"
fi

GLOBAL_EMBED=${DIRECTORY}/embed/word2vec-google-news-300
DATA_DIRECTORY=${DIRECTORY}
DATA_OUT=${CUR_EXP}
MODEL_DIRECTORY=${DIRECTORY}/models/${CUR_EXP}
mkdir -p ${MODEL_DIRECTORY}

if [[ -z "${GLOBAL_EMBED}" ]]; then
  GLOBAL_EMBED=${DIRECTORY}/embed/word2vec-google-news-300
  echo "GLOBAL_EMBED path is not set. Maybe run download_global_embeddings.sh first?"
  echo "The default is: "${GLOBAL_EMBED}
fi

mkdir -p ${DIRECTORY}/embed
cd ${DIRECTORY}
cat *.en >${DIRECTORY}/embed/corpus_contaminated.en && cat *.sen >${DIRECTORY}/embed/corpus_contaminated.sen
cat train.en >${DIRECTORY}/embed/corpus.en && cat train.sen >${DIRECTORY}/embed/corpus.sen
cd /workspace/src
python train_word2vec.py ${DIRECTORY}/embed/corpus_contaminated.en 200
python train_word2vec.py ${DIRECTORY}/embed/corpus_contaminated.sen 200
python train_word2vec.py ${DIRECTORY}/embed/corpus.en 200
python train_word2vec.py ${DIRECTORY}/embed/corpus.sen 200

cd $OPENNMT_PATH

th preprocess.lua -train_src ${DIRECTORY}/train.en -train_tgt ${DIRECTORY}/train.sen -valid_src ${DIRECTORY}/dev.en -valid_tgt ${DIRECTORY}/dev.sen -save_data ${DIRECTORY}/${DATA_OUT} -src_seq_length 80 -tgt_seq_length 80  -shuffle 1 -log_file ${DIRECTORY}/${DATA_OUT}.log -src_vocab_size 50000 -tgt_vocab_size 50000 -log_level DEBUG


th tools/concat_embedding.lua -dict_file ${DIRECTORY}/${CUR_EXP}.src.dict -global_embed ${GLOBAL_EMBED} -local_embed ${DIRECTORY}/embed/corpus_contaminated.sen.bin -save_data ${DIRECTORY}/embed/sen-embeddings-mismatched-contaminated-${CUR_EXP}
th tools/concat_embedding.lua -dict_file ${DIRECTORY}/${CUR_EXP}.tgt.dict -global_embed ${GLOBAL_EMBED} -local_embed ${DIRECTORY}/embed/corpus_contaminated.en.bin -save_data ${DIRECTORY}/embed/en-embeddings-mismatched-contaminated-${CUR_EXP}

th tools/concat_embedding.lua -dict_file ${DIRECTORY}/${CUR_EXP}.tgt.dict -global_embed ${GLOBAL_EMBED} -local_embed ${DIRECTORY}/embed/corpus_contaminated.sen.bin -save_data ${DIRECTORY}/embed/sen-embeddings-contaminated-${CUR_EXP}
th tools/concat_embedding.lua -dict_file ${DIRECTORY}/${CUR_EXP}.src.dict -global_embed ${GLOBAL_EMBED} -local_embed ${DIRECTORY}/embed/corpus_contaminated.en.bin -save_data ${DIRECTORY}/embed/en-embeddings-contaminated-${CUR_EXP}

th tools/concat_embedding.lua -dict_file ${DIRECTORY}/${CUR_EXP}.src.dict -global_embed ${GLOBAL_EMBED} -local_embed ${DIRECTORY}/embed/corpus.sen.bin -save_data ${DIRECTORY}/embed/sen-embeddings-mismatched-${CUR_EXP}
th tools/concat_embedding.lua -dict_file ${DIRECTORY}/${CUR_EXP}.tgt.dict -global_embed ${GLOBAL_EMBED} -local_embed ${DIRECTORY}/embed/corpus.en.bin -save_data ${DIRECTORY}/embed/en-embeddings-mismatched-${CUR_EXP}

th tools/concat_embedding.lua -dict_file ${DIRECTORY}/${CUR_EXP}.tgt.dict -global_embed ${GLOBAL_EMBED} -local_embed ${DIRECTORY}/embed/corpus.sen.bin -save_data ${DIRECTORY}/embed/sen-embeddings-${CUR_EXP}
th tools/concat_embedding.lua -dict_file ${DIRECTORY}/${CUR_EXP}.src.dict -global_embed ${GLOBAL_EMBED} -local_embed ${DIRECTORY}/embed/corpus.en.bin -save_data ${DIRECTORY}/embed/en-embeddings-${CUR_EXP}

cd $CWD
