from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

documents = [
    "Machine learning is a relevant branch of artificial intelligence",
    "Deep learning is a subfield of machine learning",
    "Finance and stock market predictions using AI"
]
query = "Machine learning AI"

vectorizer = CountVectorizer()
term_freq_matrix = vectorizer.fit_transform(documents + [query])
terms = vectorizer.get_feature_names_out()

df_tf = pd.DataFrame(term_freq_matrix.toarray(), index=["D1", "D2", "D3", "Query"], columns=terms)

df_tf = df_tf.div(df_tf.sum(axis=1), axis=0)

# Compute IDF
idf_transformer = TfidfTransformer(use_idf=True)
idf_transformer.fit(term_freq_matrix)
idf_values = idf_transformer.idf_
df_idf = pd.DataFrame([idf_values], columns=terms, index=["IDF"])

# Compute TF-IDF Weights
df_tfidf = df_tf * df_idf.values

# Interpretation of the Term-Document Matrix
print("TF-IDF Term-Document Matrix:")
print(df_tfidf)

#  Cosine Similarity
matrix = df_tfidf.to_numpy()
# Exclude query row
doc_matrix = matrix[:-1] 
query_vector = matrix[-1].reshape(1, -1)

cosine_sim = cosine_similarity(query_vector, doc_matrix)[0]

# Ranking documents based on similarity scores
doc_ranking = sorted(enumerate(cosine_sim), key=lambda x: x[1], reverse=True)

print("\nRanking of Documents:")
for rank, (index, score) in enumerate(doc_ranking, start=1):
    print(f"Rank {rank}: Document {index + 1} (Score: {score:.4f})")
