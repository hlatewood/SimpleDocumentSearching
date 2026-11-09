import math
from collections import Counter
import time

with open("docs.txt", "r") as f:
    documents = f.readlines()

with open("queries.txt", "r") as f:
    queries = f.readlines()

dictionary = set()
for doc in documents:
    words = doc.split()
    for word in words:
        dictionary.add(word)

dictionary = sorted(dictionary)
print("Words in dictionary:", len(dictionary))

inverted_index = {}
for word in dictionary:
    inverted_index[word] = []

for doc_id, doc in enumerate(documents, start=1):
    words = doc.split()
    for word in words:
        if doc_id not in inverted_index[word]:
            inverted_index[word].append(doc_id)

for query in queries:
    query = query.strip()
    query_words = query.split()
    print("Query: ", query)

    relevant_docs = None
    for word in query_words:
        if word in inverted_index:
            if relevant_docs is None:
                relevant_docs = set(inverted_index[word])
            else:
                relevant_docs = relevant_docs.intersection(set(inverted_index[word]))

    if relevant_docs is None:
        relevant_docs = set()

    print("Relevant documents:", *(relevant_docs))

    query_words_set = set(query_words)

    angles = []
    for doc_id in relevant_docs:
        doc_words = documents[doc_id - 1].split()
        doc_word_count = Counter(doc_words)

        relevant_words = set(doc_word_count.keys() | query_words_set)

        dot_product = 0
        doc_magnitude = 0
        query_magnitude = 0

        for word in relevant_words:
            doc_count = doc_word_count.get(word, 0)
            if word in query_words:
                query_count = 1
            else:
                query_count = 0

            dot_product += doc_count * query_count
            doc_magnitude += doc_count ** 2
            query_magnitude += query_count ** 2

        doc_magnitude = math.sqrt(doc_magnitude)
        query_magnitude = math.sqrt(query_magnitude)

        cosine = dot_product / (doc_magnitude * query_magnitude)
        cosine = max(-1.0, min(1.0, cosine))
        angle = math.degrees(math.acos(cosine))
        angles.append((doc_id, angle))
    
    angles.sort(key=lambda x: x[1])

    for doc_id, angle in angles:
        print(doc_id, f"{angle:.5f}")