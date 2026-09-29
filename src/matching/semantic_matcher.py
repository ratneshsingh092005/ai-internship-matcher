from src.embeddings.embedding_service import embed_texts
from src.matching.ranking import similarity_to_score
from src.vector_store.faiss_index import search



def retrieve_matches(index, resume_text: str, top_k: int = 10):
    embedding = embed_texts([resume_text])[0]
    scores, indices = search(index, embedding, top_k)
    return embedding, [(idx, similarity_to_score(score), score) for idx, score in zip(indices, scores) if idx >= 0]
