from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

# Detect similar texts having different labels
def detect_mismatch(texts, labels):
    embeddings = model.encode(texts)

    issues = []

    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            sim = cosine_similarity(
                [embeddings[i]],
                [embeddings[j]]
            )[0][0]

            if sim > 0.85 and labels[i] != labels[j]:
                issues.append({
                    "Text 1": texts[i],
                    "Text 2": texts[j],
                    "Label 1": labels[i],
                    "Label 2": labels[j],
                    "Similarity": round(sim, 2)
                })

    return issues


# Detect semantic duplicates
def detect_semantic_duplicates(df, text_column):
    texts = df[text_column].astype(str).tolist()

    embeddings = model.encode(texts)

    results = []

    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            sim = cosine_similarity(
                [embeddings[i]],
                [embeddings[j]]
            )[0][0]

            if sim > 0.85:
                results.append({
                    "Text 1": texts[i],
                    "Text 2": texts[j],
                    "Similarity": round(sim, 2)
                })

    return results