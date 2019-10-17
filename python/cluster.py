import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from os.path import join
import pickle
from sklearn.cluster import KMeans
from constants import PROCESSED_RECORDS_FILENAME, TERM_DOCUMENT_MATRIX_FILENAME
from utils import get_data_path
from sklearn.decomposition import TruncatedSVD


def plot_kmean_results(result_dict):
    """
    plot the results of kmeans clustering

    input:
        result_dict: with mapping of 'number of clusters':'within cluster ss'
    """
    #Plot the elbow curve
    plt.plot(list(result_dict.keys()), list(result_dict.values()), 'bx-')
    plt.xlabel('k')
    plt.ylabel('within cluster ss')


def append_to_csv(filename, l):
        with open(filename, 'a') as f:
            f.write(','.join(str(a) for a in l)+'\n')


def kmeans_original():
    #Import iati.identifier csv for records included in doc-term matrix
    df1 = pd.read_csv(join(get_data_path(), PROCESSED_RECORDS_FILENAME), encoding='iso-8859-1') 
    df1 = df1[['iati.identifier']]


    #Import Pickle file (need both IATI dataframe and term document matrix to be read in for this script)
    with open(join(get_data_path(), TERM_DOCUMENT_MATRIX_FILENAME), "rb") as _file:
        X = pickle.load(_file)

    #if want to look at X
    #pd.DataFrame(X.toarray(), columns = vectorizer.get_feature_names()).head()
    #shape of term-document matrix
    #X.toarray().shape
    
    
    #Test with n clusters (n_jobs -1 means max processes spawned)

    for n_clust in range(5, 105, 5):
        km = KMeans(n_clusters=n_clust, n_jobs=-1)
        start = time.time()
        clusters = km.fit(X)
        end = time.time()
        print("{0} clusters: time elapsed: {1} seconds".format(n_clust, end - start))
        
        #within cluster sum of squares
        append_to_csv(os.path.join(wd,'ssResults.csv'), [n_clust, clusters.inertia_]) 
    # print("{0} clusters: within cluster ss: {1}".format(n_clust, clusters.inertia_))

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
        
        #write cluster centroids to pickle file
        with open(os.path.join(wd, 'clusterCentroidsDict{0}.pkl'.format(n_clust)), 'wb') as out:
            pickle.dump(clusters.cluster_centers_, out)



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
    plot_kmean_results(result_dict)


def kmeans_svd():
    #Import iati.identifier csv for records included in doc-term matrix
    df1 = pd.read_csv(join(get_data_path(), PROCESSED_RECORDS_FILENAME), encoding='iso-8859-1') 
    df1 = df1[['iati.identifier']]


    #Import Pickle file (need both IATI dataframe and term document matrix to be read in for this script)
    with open(join(get_data_path(), TERM_DOCUMENT_MATRIX_FILENAME), "rb") as _file:
        X = pickle.load(_file)

    #Apply SVD. n_components = 100 is recommended for LSA according to scikit help doc:
    # https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html
    start = time.time()
    
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

    plot_kmean_results(result_dict)

    with open(os.path.join(wd, 'clusterElbowResSVD.pkl'), 'wb') as out:
        pickle.dump(result_dict, out)


if __name__ = "__main__":
    pass