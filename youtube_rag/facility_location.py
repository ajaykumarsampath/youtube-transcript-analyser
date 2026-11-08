import numpy as np

def facility_location_mmr(embeddings,top_k=10):
    # Cosine similarity
    similarity = embeddings @ embeddings.T

    # Ignore negative similarities
    similarity = np.maximum(similarity, 0)

    n = len(embeddings)

    selected = []
    current_coverage = np.zeros(n)

    candidates = set(range(n))

    for _ in range(min(top_k, n)):

        best_idx = None
        best_gain = -np.inf

        for idx in candidates:

            # Coverage after adding candidate
            new_coverage = np.maximum(
                current_coverage,
                similarity[:, idx]
            )

            gain = (
                new_coverage.sum()
                - current_coverage.sum()
            )

            if gain > best_gain:
                best_gain = gain
                best_idx = idx

        selected.append(best_idx)

        current_coverage = np.maximum(
            current_coverage,
            similarity[:, best_idx]
        )

        candidates.remove(best_idx)

    return selected


# selected = facility_location_mmr(
#     embeddings,
#     top_k=15
# )
#
# selected.sort()
#
# summary_sentences = [
#     sentences[i] for i in selected
# ]