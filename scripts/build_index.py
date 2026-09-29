from pathlib import Path
import joblib
from src.data.loader import load_internships
from src.embeddings.embedding_service import embed_texts, MODEL_NAME
from src.vector_store.faiss_index import build_index, save_metadata

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "internships.csv"
MODELS = ROOT / "models"


def main():
    df = load_internships(DATA)
    texts = (df["title"] + ". " + df["description"] + ". Skills: " + df["skills"]).tolist()
    embeddings = embed_texts(texts)
    build_index(embeddings, MODELS / "internship_index.faiss")
    metadata = df.to_dict(orient="records")
    save_metadata(metadata, MODELS / "internship_metadata.joblib")
    joblib.dump({"model": MODEL_NAME, "dimension": 384, "normalized": True}, MODELS / "embedding_config.joblib")
    print(f"Built FAISS index with {len(df)} internships.")


if __name__ == "__main__":
    main()
