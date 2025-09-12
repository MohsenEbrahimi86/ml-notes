**FAISS** (Facebook AI Similarity Search) is an open-source library developed by **Meta (formerly Facebook)** for efficient **similarity search** and **clustering** of dense vectors. It is specifically designed to handle large-scale vector datasets — often millions or even billions of high-dimensional vectors — with high speed and low memory usage.

### Key Features of FAISS:

1. **Efficient Nearest Neighbor Search**:

   - Finds the _k_-nearest neighbors (k-NN) of a query vector in a large dataset.
   - Optimized for **L2 distance** (Euclidean) and **inner product** (cosine similarity) metrics.

2. **Supports Multiple Index Types**:

   - **Exact search**: Brute-force (for small datasets).
   - **Approximate search**: Uses advanced techniques like:
     - **Inverted File Index (IVF)**: Partitions vectors into clusters for faster search.
     - **Product Quantization (PQ)**: Compresses vectors to reduce memory and speed up computation.
     - **Hierarchical Navigable Small World (HNSW)**: Graph-based indexing for high accuracy and speed.

3. **GPU Acceleration**:

   - FAISS supports NVIDIA GPUs via CUDA, enabling massive speedups for large-scale searches.

4. **Memory Efficient**:

   - Uses quantization and compression techniques to store large vector databases in limited memory.

5. **Scalable**:

   - Can handle datasets ranging from thousands to **billions** of vectors.

6. **Language Bindings**:
   - Primarily written in C++, with Python bindings for ease of use.
   - Also available in Java, Go, and Rust via community ports.

---

### Common Use Cases:

- **Semantic Search**: Finding similar text embeddings (e.g., from BERT, Sentence-BERT).
- **Recommendation Systems**: Finding items similar to a user’s preferences.
- **Deduplication**: Detecting near-duplicate images, documents, or audio clips.
- **Retrieval-Augmented Generation (RAG)**: Retrieving relevant context from knowledge bases for LLMs.
- **Image/Video Retrieval**: Matching visual features extracted by CNNs.

---

### Example (Python):

```python
import faiss
import numpy as np

# Generate random 128-dimensional vectors
d = 128  # dimension
nb = 100000  # database size
nq = 1000    # number of queries

np.random.seed(1234)
xb = np.random.random((nb, d)).astype('float32')
xq = np.random.random((nq, d)).astype('float32')

# Build index
index = faiss.IndexFlatL2(d)  # L2 distance
index.add(xb)                 # add vectors to index

# Search
k = 4                         # return 4 nearest neighbors
D, I = index.search(xq, k)    # D: distances, I: indices

print(I[0])  # indices of 4 closest vectors to first query
```

---

### Why FAISS?

Before FAISS, performing approximate nearest neighbor search on billion-scale datasets was computationally prohibitive. FAISS made it practical by combining smart indexing, quantization, and GPU acceleration — becoming the **de facto standard** in production systems at Meta, Netflix, Spotify, and many AI startups.

🔗 Official GitHub: https://github.com/facebookresearch/faiss  
📚 Documentation: https://faiss.ai/

In short, **FAISS is the go-to tool when you need to quickly find “similar” things represented as vectors** — especially at scale.
