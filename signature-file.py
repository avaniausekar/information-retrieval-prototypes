import hashlib

# using 16 bit for simplicity
# can use 64, 128 so on for very large files
# TODO what about hash collisions ?
# Why isn't SHA256 working for this ??

def hash_word(word, bit_len=16):
    hash_val = int(hashlib.md5(word.encode()).hexdigest(), 16)
    return hash_val % bit_len

def create_sign(doc, bit_len=16):
    sign = 0
    words = doc.lower().split()
    for word in words:
        bit_pos = hash_word(word, bit_len)
        # Setting the bit position
        sign |= (1 << bit_pos)  
    return sign

def search(query, doc_sign, bit_len=16):
    query_sign = create_sign(query, bit_len)
    res = []
    for i, doc_sig in enumerate(doc_sign):
        if (query_sign & doc_sig) == query_sign:
            res.append(f"Doc{i+1}")
    return res if res else ["No match"]

documents = [
    "Information retrieval is powerful",
    "Retrieval uses indexing techniques",
    "Efficient retrieval depends on indexing"
]

doc_signs = [create_sign(doc) for doc in documents]
print("Sinatures: ",doc_signs)

query = "retrieval indexing"
match = search(query, doc_signs)
print("Matching Documents:", match)
