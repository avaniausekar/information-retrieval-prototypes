# This is just an understanding of how bm2 okapi works
import math
import re
from collections import Counter
from typing import List, Dict, Tuple

class BM25:

    def __init__(self, documents: List[str], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1  # Controls term frequency saturation point
        # Controls length normalization (0-1, where 0=no normalization, 1=full normalization)
        self.b = b
        self.documents = documents
        self.doc_count = len(documents)

        # Preprocess
        self.tokenized_docs = [self.tokenize(doc) for doc in documents]
        self.doc_lengths = [len(doc) for doc in self.tokenized_docs]
        self.avg_doc_length = sum(self.doc_lengths) / \
            self.doc_count if self.doc_count > 0 else 0

        # Build inverted index and calculate IDF scores
        self.vocab = set()
        self.doc_term_freqs = []

        for doc_tokens in self.tokenized_docs:
            term_freq = Counter(doc_tokens)
            self.doc_term_freqs.append(term_freq)
            self.vocab.update(term_freq.keys())

        self.idf_scores = self.calculate_idf()

    def tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        # print(tokens)
        return tokens

    def calculate_idf(self) -> Dict[str, float]:
        # Calculate (IDF)
        # IDF(term) = log((N - df(term) + 0.5) / (df(term) + 0.5))
        # N = total docs
        idf_scores = {}

        for term in self.vocab:
            # Count documents containing the term
            doc_freq = sum(
                1 for doc_terms in self.doc_term_freqs if term in doc_terms)

            # BM25 IDF formula
            idf = math.log((self.doc_count - doc_freq + 0.5) /
                           (doc_freq + 0.5))
            idf_scores[term] = idf

        return idf_scores

    def calculate_bm25(self, query_terms: List[str], doc_idx: int) -> float:
        # BM25(D,Q) = Σ IDF(qi) * (f(qi,D) * (k1 + 1)) / (f(qi,D) + k1 * (1 - b + b * |D|/avgdl))
        # f(qi,D) = frequency of term qi in document D
        # D = length of document D
        # avgdl = average document length
        score = 0.0
        doc_terms = self.doc_term_freqs[doc_idx]
        doc_length = self.doc_lengths[doc_idx]

        for term in query_terms:
            if term not in self.vocab:
                continue

            # Term frequency in document
            tf = doc_terms.get(term, 0)

            if tf > 0:
                # IDF component
                idf = self.idf_scores[term]

                # BM25 formula components
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * \
                    (1 - self.b + self.b * (doc_length / self.avg_doc_length))

                score += idf * (numerator / denominator)

        return score

    def search(self, query: str, top_k: int = 10) -> List[Tuple[int, float, str]]:
        query_terms = self.tokenize(query)
        if not query_terms:
            return []

        # Calculate BM25 scores for all documents
        scores = []
        for doc_idx in range(self.doc_count):
            score = self.calculate_bm25(query_terms, doc_idx)
            scores.append((doc_idx, score, self.documents[doc_idx]))

        # Sort by scor
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def get_term_stats(self, term: str) -> Dict:
        if term not in self.vocab:
            return {"exists": False}

        doc_freq = sum(
            1 for doc_terms in self.doc_term_freqs if term in doc_terms)
        total_freq = sum(doc_terms.get(term, 0)
                         for doc_terms in self.doc_term_freqs)

        return {
            "exists": True,
            "document_frequency": doc_freq,
            "total_frequency": total_freq,
            "idf_score": self.idf_scores[term]
        }


def main():
    # Samples
    documents = [
        "The quick brown fox jumps over the lazy dog",
        "Machine learning is a subset of artificial intelligence",
        "Python is a popular programming language for data science",
        "Natural language processing helps computers understand human language",
        "Information retrieval systems help users find relevant documents",
        "Search engines use ranking algorithms like BM25 to order results",
        "The brown fox is quick and agile in the forest",
        "Data science involves statistics, programming, and domain expertise",
        "Avani tries to implement some common algorithms"
    ]

    bm25 = BM25(documents)

    queries = [
        "brown fox",
        "machine learning",
        "programming language",
        "search ranking",
        "avani"
    ]
    print("BM25 Search Results")
    print("=" * 50)

    for query in queries:
        print(f"\nQuery: '{query}'")
        print("-" * 30)

        results = bm25.search(query, top_k=3)

        for rank, (doc_idx, score, doc_text) in enumerate(results, 1):
            print(f"{rank}. Score: {score:.4f}")
            print(f"   Document: {doc_text}")

        if not results:
            print("No results found.")

    print(f"\n\nTerm Statistics")
    print("=" * 50)

    sample_terms = ["brown", "machine", "programming", "xyz", "avani"]
    for term in sample_terms:
        stats = bm25.get_term_stats(term)
        print(f"Term: '{term}' -> {stats}")

main()