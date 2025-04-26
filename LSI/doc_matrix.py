import numpy as np

def doc_to_matrix(documents):
    processed_docs = [preprocess(doc) for doc in documents]

    vocab = sorted(list(set(word for doc in processed_docs for word in doc)))
    vocab_index = {word: idx for idx, word in enumerate(vocab)}

    print("Vocabulary:")
    print(vocab)

    term_doc_mat = np.zeros((len(vocab), len(documents)))

    for doc_idx, doc in enumerate(processed_docs):
        for word in doc:
            word_idx = vocab_index[word]
            term_doc_mat[word_idx, doc_idx] += 1
    print("\nTerm-Document Matrix:")
    print(term_doc_mat)
    return term_doc_mat

def preprocess(doc):
    return doc.lower().split()

# documents = [
#     "the cat and the hat",
#     "the quick brown fox",
#     "the dog barked at the mailman",
#     "cats and dogs are friendly pets",
#     "foxes are wild animals",
# ]


