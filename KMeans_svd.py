# -*- coding: utf-8 -*-
"""
IATI Partner Search SVD and K-means
1) Read pickle file of term document matrix and csv of iatiids used
2) Reduce dimensions using SVD
3) K-means on matrix with reduced dimensions
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import os
from sklearn.cluster import KMeans

wd = ''

#Import iati.identifier csv for records included in doc-term matrix

df1 = pd.read_csv(os.path.join(wd,'all_used_records_stemEngDict.csv'), encoding='iso-8859-1') 
df1 = df1[['iati.identifier']]


#Import pickle file of full document-term matrix
import pickle
pklfile = os.path.join(wd, 'iatiFullTDMstemEngDict.pkl')
X = pickle.load(open(pklfile,'rb'))
X.close()

#Apply SVD. n_components = 100 is recommended for LSA according to scikit help doc:
# https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html
start = time.time()
from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD(n_components=100, n_iter=5, random_state=42)
X = svd.fit_transform(X)
end = time.time()
print("SVD time elapsed: {0} seconds".format(end - start))

#Check dimensions reduced to n_components
#print(X.shape)

#Test with n clusters (n_jobs -1 means max processes spawned)
n_clust_list =[10,20,30,40,50,60]
for n_clust in n_clust_list:
    km = KMeans(n_clusters=n_clust, n_jobs=-1)
    start = time.time()
    clusters = km.fit(X)
    end = time.time()
    print("{0} clusters: time elapsed: {1} seconds".format(n_clust, end - start))
    #within cluster sum of squares
    print("{0} clusters: within cluster ss: {1}".format(n_clust, clusters.inertia_))

#Show counts per cluster number
#print(np.unique(clusters.labels_, return_counts=True))

#Check same number of documents returned
#print(np.unique(clusters.labels_, return_counts=True)[1].sum())

#Show number of iterations of K-means
#print("number of iterations: {0}".format(clusters.n_iter_))
    
    
    #add the cluster number to each input iati record
    df1.insert(df1.shape[1], 'cluster{0}'.format(n_clust), clusters.labels_)
    
#Show number of records by organisation by cluster
#print(df1.groupby(['participating.org..Implementing.','cluster{0}'.format(n_clust)]).size())
    
    #Write cluster assigned to each iati.identifier out to csv
    df1[['iati.identifier', 'cluster{0}'.format(n_clust)]].to_csv(os.path.join(wd,'iati{0}ClustersSVD.csv'.format(n_clust)), encoding='iso-8859-1', index=False)

#####################################################################################################
#Elbow curve...
#try number of clusters 1- 25 and add sum of squares to dict (takes about 10-15 mins on DFID laptop)
start = time.time()

result_dict = {}

for i in range(5, 60, 5):
    km = KMeans(n_clusters=i)
    clusters = km.fit(X)
    result_dict[i] = clusters.inertia_
    end = time.time()
    print("{0} clusters - time elapsed: {1} seconds".format(i, end - start))

#Plot the elbow curve
plt.plot(list(result_dict.keys()), list(result_dict.values()), 'bx-')
plt.xlabel('k')
plt.ylabel('within cluster ss')

with open(os.path.join(wd, 'clusterElbowResSVD.pkl'), 'wb') as out:
    pickle.dump(result_dict, out)
