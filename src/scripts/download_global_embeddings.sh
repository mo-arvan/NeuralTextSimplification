#!/bin/bash
source ./base_conf.sh
EMBED_DIR=${DIRECTORY}/embed/
mkdir -p $EMBED_DIR
cd $EMBED_DIR
wget 'https://github.com/RaRe-Technologies/gensim-data/releases/download/word2vec-google-news-300/word2vec-google-news-300.gz'
#cp ../GoogleNews-vectors-negative300.bin.gz . &&
gunzip GoogleNews-vectors-negative300.bin.gz
