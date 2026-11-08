# Maximal Marginal Relevance
from typing import Any

import numpy as np
import networkx as nx


def mmr_summary(
        sentences: list[str],  relevance: np.ndarray, similarity_matrix: np.ndarray, top_k=3,
        lambda_param=0.7
) -> tuple[list[float], list[str]]:
    """Select sentences using Maximal Marginal Relevance (MMR)"""
    selected = []
    remaining = list(range(len(sentences)))

    while remaining and len(selected) < top_k:

        if not selected:
            # Select the most relevant sentence first
            best_idx = max(remaining, key=lambda i: relevance[i])
        else:
            mmr_scores = {}

            for i in remaining:
                redundancy = max(similarity_matrix[i, j] for j in selected)

                mmr_scores[i] = lambda_param * relevance[i]- (1 - lambda_param) * redundancy

            # best_idx = max(mmr_scores, key=mmr_scores.get)
            best_idx, _ = max(mmr_scores.items(), key=lambda x: x[1])

        selected.append(best_idx)
        remaining.remove(best_idx)

    selected.sort()

    return [relevance[i] for i in selected], [sentences[i] for i in selected]


def summary_facility_location(
        sentences: list[str], similarity: np.ndarray, relevance: np.ndarray, top_k: int= 5
) -> list[str]:
    """Select sentences using Maximal Marginal Relevance (MMR) with facility location function"""
    # Cosine similarity
    # similarity = embeddings @ embeddings.T

    # Ignore negative similarities
    similarity = np.maximum(similarity, 0)

    n_size = len(sentences)

    selected = []
    current_coverage = np.zeros(n_size)

    candidates = set(range(n_size))

    for _ in range(min(top_k, n_size)):

        best_idx = None
        best_gain = -np.inf

        for idx in candidates:

            # Coverage after adding candidate
            new_coverage = np.maximum(current_coverage, similarity[:, idx])

            # gain = new_coverage.sum() - current_coverage.sum()
            gain = (
                relevance*(new_coverage - current_coverage)
            ).sum()

            if gain > best_gain:
                best_gain = gain
                best_idx = idx

        selected.append(best_idx)

        current_coverage = np.maximum(current_coverage, similarity[:, best_idx])

        candidates.remove(best_idx)

    # return selected
    selected.sort()
    return [sentences[i] for i in selected]


def network_summary(sentences: list[str], similarity_matrix: np.ndarray, top_k: int=3) -> tuple[
    list[float], list[str]]:
    # Remove self-similarity
    similarity_matrix[
        range(similarity_matrix.shape[0]),
        range(similarity_matrix.shape[0])
    ] = 0

    # Construct the sentence graph
    graph = nx.from_numpy_array(similarity_matrix)

    # Rank sentences
    textrank_scores = nx.pagerank(graph, weight="weight")

    # Select the top 3 sentences
    ranked_indices = sorted(textrank_scores, key=textrank_scores.get, reverse=True)[:top_k]

    # Restore original order
    ranked_indices.sort()

    return [textrank_scores[i] for i in ranked_indices], [sentences[i] for i in ranked_indices]


def semantic_similarities(
        sentences: list[str], sentence_embedding: np.ndarray, document_embedding: np.ndarray, top_k: int
) -> tuple[list[float | int], list[str]]:
    # Score each sentence by similarity to the document representation
    semantic_scores = sentence_embedding @ document_embedding

    # Select the top 3 sentences
    ranked_indices = np.argsort(semantic_scores)[::-1][:top_k]

    # Restore original order
    ranked_indices = sorted(ranked_indices)

    # for i in ranked_indices:
    #     print(f"{semantic_scores[i]:.4f} | {sentences[i]}")

    return [semantic_scores[i].item() for i in ranked_indices], [sentences[i] for i in ranked_indices]


def semantic_summary(sentences: list[str], embeddings: np.ndarray, top_k: int=3) -> tuple[list[float], list[str]]:
    # Represent the document using its average sentence embedding
    document_embedding = embeddings.mean(axis=0)

    document_embedding /= (
            np.linalg.norm(document_embedding) + 1e-12
    )

    # Score each sentence by similarity to the document representation
    semantic_scores = embeddings @ document_embedding

    # Select the top 3 sentences
    ranked_indices = np.argsort(semantic_scores)[::-1][:top_k]

    # Restore original order
    ranked_indices = sorted(ranked_indices)

    return [round(semantic_scores[i].item(), 3) for i in ranked_indices], [sentences[i] for i in ranked_indices]
