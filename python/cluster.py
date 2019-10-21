import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from os.path import join
import pickle
from sklearn.cluster import KMeans
from constants import (
    PROCESSED_RECORDS_FILENAME,
    TERM_DOCUMENT_MATRIX_FILENAME,
    CLUSTERING_SUM_OF_SQUARE_COMPARISON_FILENAME,
    CLUSTER_CENTROIDS_FILENAME_CONVENTION,
    ACTIVITY_CLUSTER_ASSIGNMENT_FILENAME_CONVENTION,
)
from utils import get_data_path
from sklearn.decomposition import TruncatedSVD


def plot_kmean_results(result_dict):
    """
    plot the results of kmeans clustering

    input:
        result_dict: with mapping of 'number of clusters':'within cluster ss'
    """
    # Plot the elbow curve
    plt.plot(list(result_dict.keys()), list(result_dict.values()), "bx-")
    plt.xlabel("k")
    plt.ylabel("within cluster ss")


def append_to_csv(filename, l):
    with open(filename, "a") as _file:
        _file.write(",".join(str(a) for a in l) + "\n")


def apply_svd(term_document_matrix_dataframe, number_of_components=100):
    start = time.time()
    svd = TruncatedSVD(n_components=number_of_components, n_iter=5, random_state=42)
    svd_term_document_matrix_dataframe = svd.fit_transform(
        term_document_matrix_dataframe
    )
    end = time.time()
    print("SVD time elapsed: {0} seconds".format(end - start))

    return svd_term_document_matrix_dataframe


def kmeans_clustering(
    term_document_matrix_dataframe,
    term_dataframe,
    minimum_number_of_clusters,
    maximum_number_of_clusters,
    increment,
):
    # Apply SVD. n_components = 100 is recommended for LSA according to scikit help doc:
    # https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html
    start = time.time()

    # Check dimensions reduced to n_components
    # print(term_document_matrix_dataframe.shape)

    result_dict = {}

    # Test with n clusters (n_jobs -1 means max processes spawned)
    for n_clust in range(
        minimum_number_of_clusters, maximum_number_of_clusters, increment
    ):
        km = KMeans(n_clusters=n_clust, n_jobs=-1)
        start = time.time()
        clusters = km.fit(term_document_matrix_dataframe)
        result_dict[n_clust] = clusters.inertia_
        end = time.time()
        print("{0} clusters: time elapsed: {1} seconds".format(n_clust, end - start))

        # within cluster sum of squares
        print("{0} clusters: within cluster ss: {1}".format(n_clust, clusters.inertia_))
        append_to_csv(
            join(get_data_path(), CLUSTERING_SUM_OF_SQUARE_COMPARISON_FILENAME),
            [n_clust, clusters.inertia_],
        )

        term_dataframe.insert(term_dataframe.shape[1], 'cluster{0}'.format(n_clust), clusters.labels_)
        # Write cluster assigned to each iati.identifier out to csv
        term_dataframe[["iati.identifier", "cluster{0}".format(n_clust)]].to_csv(
            join(
                get_data_path(),
                ACTIVITY_CLUSTER_ASSIGNMENT_FILENAME_CONVENTION.format(n_clust),
            ),
            encoding="iso-8859-1",
            index=False,
        )

        with open(
            join(
                get_data_path(), CLUSTER_CENTROIDS_FILENAME_CONVENTION.format(n_clust)
            ),
            "wb",
        ) as out:
            pickle.dump(clusters.cluster_centers_, out)


# these functions can be used to explore specific clustering attributes
# can be removed if desired


def get_term_document_matrix_shape(tdm):
    return tdm.shape


def show_counts_per_cluster_number(clusters):
    return np.unique(clusters.labels_, return_counts=True)


def check_same_number_of_documents_returned(clusters):
    return np.unique(clusters.labels_, return_counts=True)[1].sum()


def get_number_of_iterations_of_kmeans(clusters):
    return clusters.n_iter_


def get_number_of_records_by_organisation_by_cluster(term_dataframe, n_clust):
    return term_dataframe.groupby(
        ["participating.org..Implementing.", "cluster{0}".format(n_clust)]
    ).size()


if __name__ == "__main__":
    # Import iati.identifier csv for records included in doc-term matrix
    term_dataframe = pd.read_csv(
        join(get_data_path(), PROCESSED_RECORDS_FILENAME), encoding="iso-8859-1"
    )
    term_dataframe = term_dataframe[["iati.identifier"]]

    # Import Pickle file (need both IATI dataframe and term document matrix to be read in for this script)
    with open(join(get_data_path(), TERM_DOCUMENT_MATRIX_FILENAME), "rb") as _file:
        term_document_matrix_dataframe = pickle.load(_file)

    minimum_number_of_clusters = 10
    maximum_number_of_clusters = 15
    increment = 2

    # Apply SVD to TDM
    svd_term_document_matrix_dataframe = apply_svd(term_document_matrix_dataframe)

    # cluster over range of clusters
    kmeans_clustering(
        # change this to term_document_matrix_dataframe if you don't want to use SVD
        svd_term_document_matrix_dataframe,
        term_dataframe,
        minimum_number_of_clusters,
        maximum_number_of_clusters,
        increment,
    )
