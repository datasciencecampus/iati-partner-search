# -*- coding: utf-8 -*-
"""
Top tf-idf word per IATI record grouped by K-means cluster

"""
import pandas as pd
import pickle
import os
import numpy as np

wd = r"C:\Users\t-wilson\Documents\IATI_partner_search\download_stemEngDict"

# 1 Read the pickle file for document term matrix into X
with open(os.path.join(wd, "iatiFullTDMstemEngDict.pkl"), "rb") as f:
    X = pickle.load(f)

# 2 Get the word list
words_df = pd.read_csv(os.path.join(wd, "wordsListStemEngDict.csv"), names=["word"])
words = words_df["word"].tolist()

# 3 Get the iati records used for this pre-processing set
clusters_df = pd.read_csv(os.path.join(wd, "iati30Clusters.csv"), encoding="utf-8")

# 4 Get index of highest tf-idf per IATI record

maxIndex = X.argmax(axis=1)

maxIndex = np.array(maxIndex.flatten())[0]

# 5 Get word corresponding to index
outlist = []
for v in maxIndex:
    outlist.append(words[v])

# 6 Add words to cluster records
clusters_df["top_word"] = outlist

# 7 Group by on cluster, top_word
cluster_group = clusters_df.groupby(["cluster30", "top_word"]).count().reset_index()
cluster_group.columns = ["cluster30", "top_word", "count"]

# 8 Get the max word count per cluster
cluster_top = (
    cluster_group.sort_values("count")
    .drop_duplicates(["cluster30"], keep="last")
    .sort_values("cluster30")
)

# 9 write to csv
cluster_group = cluster_group.sort_values(
    ["cluster30", "count"], ascending=[True, False]
)
cluster_group.to_csv(os.path.join(wd, "all_top_words_per_cluster.csv"), index=False)
cluster_top.to_csv(os.path.join(wd, "top_word_per_cluster.csv"), index=False)
