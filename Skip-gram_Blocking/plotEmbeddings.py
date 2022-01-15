

import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

wordEmbeddings = pd.read_csv("embeddings_matrix.csv")

squishedVectors = TSNE(n_components=2, perplexity=50, init="pca", n_iter=5000).fit_transform(wordEmbeddings)

print(squishedVectors)

plt.scatter(squishedVectors[:,0], squishedVectors[:,1])
plt.show()