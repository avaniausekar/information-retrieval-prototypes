import numpy as np
import doc_matrix
# Beginner implementation of Latent Semantic Indexing

documents = [
    "the cat and the hat",
    "the quick brown fox",
    "the dog barked at the mailman",
    "cats and dogs are friendly pets",
    "foxes are wild animals",
]
term_document_matrix = doc_matrix.doc_to_matrix(documents)

print("Original Term-Document Matrix:")
print(term_document_matrix)

# Performs Singular Value Decomposition 
# TODO need to recheck this !!!
U, S, VT = np.linalg.svd(term_document_matrix, full_matrices=False)

print("\nU matrix (terms vs concepts):")
print(U)

print("\nS vector (singular values):")
print(S)

print("\nVT matrix (concepts vs documents):")
print(VT)

# Step 3: Reduce dimensions
k = 2  # right now keeping top 2 concepts
U_k = U[:, :k]
S_k = np.diag(S[:k])
VT_k = VT[:k, :]

approx_matrix = np.dot(U_k, np.dot(S_k, VT_k))

print("\nApproximate Matrix after LSI (k=2):")
print(approx_matrix)

# Step 5: LSI representation
# Each document is now represented by the rows of S_k * VT_k
doc_concepts = np.dot(S_k, VT_k)

print("\nDocuments represented in concept space:")
print(doc_concepts.T)
