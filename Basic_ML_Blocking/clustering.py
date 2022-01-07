import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram
from sklearn.datasets import load_iris
from sklearn.cluster import AgglomerativeClustering


####################################
#NEED TO UNDERSTAND THIS CODE BETTER
####################################


def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)



honeypotDF = pd.read_csv("honeypot-redundant-dropped.csv")          #dataframe

model = AgglomerativeClustering(distance_threshold=0, n_clusters=None)
model = model.fit(honeypotDF)
plt.title("Hierarchical Clustering Dendogram")
plot_dendrogram(model, truncate_mode="level", p=5)
plt.xlabel("Number of instances in node (no brackets means single instance index).")
plt.show()