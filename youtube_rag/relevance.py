import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class Relevance:
    """Calculate relevance for different type"""

    @staticmethod
    def from_tfidf_matrix(tfidf_matrix:np.ndarray) -> np.ndarray:

        relevance = np.asarray(
            tfidf_matrix.mean(axis=1)
        ).ravel()

        # Normalize relevance to [0, 1]
        if relevance.max() > relevance.min():
            relevance = (
                    (relevance - relevance.min())
                    / (relevance.max() - relevance.min())
            )
        else:
            relevance = np.ones_like(relevance)

        return relevance

    @staticmethod
    def from_similarity_matrix_for_centrality(mat: np.ndarray) -> np.ndarray:
        relevance = (mat - np.diag(np.ones(mat.shape[0]))).sum(axis=1) / (mat.shape[0] - 1)
        return relevance

    @staticmethod
    def from_embeddings(embeddings: np.ndarray, passage_embedding: np.ndarray) -> np.ndarray:
        relevance = cosine_similarity(embeddings, passage_embedding).flatten()
        return relevance

