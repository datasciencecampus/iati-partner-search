import pickle
import os
import numpy as np
from scipy import sparse
from sklearn.cluster import KMeans
import time
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD  #

wd = r"C:\Users\t-wilson\Documents\IATI_partner_search\download_stemEngDict"

# Read in pickle file of doc-term matrix
with open(os.path.join(wd, "iatiFullTDMstemEngDict.pkl"), "rb") as f:
    X = pickle.load(f)

svd = TruncatedSVD(n_components=100, n_iter=5, random_state=42)
X = svd.fit_transform(X)

# Calculate density of SVD matrix
non_zero = np.count_nonzero(X)
all_pos = X.shape[0] * X.shape[1]
dense = non_zero / all_pos
print("SVD calculated density {0}".format(dense))

# Make a random matrix of same density (too large & K-means takes forever)
testX = sparse.random(2000, 100, density=dense)

print("generated shape {0}".format(testX.shape))
print(
    "generated density {0}".format(testX.getnnz() / (testX.shape[0] * testX.shape[1]))
)


# Elbow curve...
# try number of clusters 1- 25 and add sum of squares to dict (takes about 10-15 mins on DFID laptop)
start = time.time()

result_dict = {}

for i in range(5, 60, 5):
    km = KMeans(n_clusters=i)
    clusters = km.fit(testX)
    result_dict[i] = clusters.inertia_
    end = time.time()
    print("{0} clusters - time elapsed: {1} seconds".format(i, end - start))

# Plot the elbow curve
plt.plot(list(result_dict.keys()), list(result_dict.values()), "bx-")
plt.xlabel("k")
plt.ylabel("within cluster ss")
