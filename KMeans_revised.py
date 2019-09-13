# -*- coding: utf-8 -*-
"""
IATI Partner Search K-means

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import os

wd = ''

#Import iati.identifier csv for records included in doc-term matrix
df1 = pd.read_csv(os.path.join(wd,'all_used_records_stemEngDict.csv'), encoding='iso-8859-1') 
df1 = df1[['iati.identifier']]


#Import Pickle file (need both IATI dataframe and term document matrix to be read in for this script)
import pickle
filename = os.path.join(wd,'iatiFullTDMstemEngDict.pkl')
X = pickle.load(open(filename,'rb'))

#if want to look at X
#pd.DataFrame(X.toarray(), columns = vectorizer.get_feature_names()).head()
#shape of term-document matrix
#X.toarray().shape
 
from sklearn.cluster import KMeans
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
    df1[['iati.identifier', 'cluster{0}'.format(n_clust)]].to_csv(os.path.join(wd,'iati{0}Clusters.csv'.format(n_clust)), encoding='iso-8859-1', index=False)

#####################################################################################################
#Elbow curve...
#try number of clusters 1- 25 and add sum of squares to dict (takes about 10-15 mins on DFID laptop)
#start = time.time()

#result_dict = {}

#for i in range(1, 26):
#    km = KMeans(n_clusters=i)
#    clusters = km.fit(X)
#    result_dict[i] = clusters.inertia_

#end = time.time()
#print("time elapsed: {0} seconds".format(end - start))

#Plot the elbow curve
#plt.plot(list(result_dict.keys()), list(result_dict.values()), 'bx-')
#plt.xlabel('k')
#plt.ylabel('within cluster ss')

