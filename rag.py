import faiss
import numpy as np
from pypdf import PdfReader
from embedding import embed_text
from rank_bm25 import BM25Okapi


# -------------------------------
# 📄 Load PDF
# -------------------------------
def load_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text


# -------------------------------
# ✂️ Improved Chunking (Sentence-aware)
# -------------------------------
def chunk_text(text, chunk_size=300, overlap=75):
    sentences = text.split(".")

    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        words = sentence.split()

        # If adding this sentence exceeds chunk size → push chunk
        if current_length + len(words) > chunk_size:
            chunks.append(" ".join(current_chunk))

            # Keep overlap
            current_chunk = (
                current_chunk[-overlap:]
                if overlap < len(current_chunk)
                else current_chunk
            )
            current_length = len(current_chunk)

        current_chunk.extend(words)
        current_length += len(words)

    # Add final chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


# -------------------------------
# 🧠 Hybrid Vector Store
# -------------------------------
class VectorStore:
    def __init__(self):
        self.index = None
        self.texts = []
        self.bm25 = None
        self.tokenized_chunks = []

    # ---------------------------
    # Build Index
    # ---------------------------
    def build(self, chunks):
        # Dense embeddings
        vectors = embed_text(chunks)
        dim = vectors.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(vectors).astype("float32"))

        self.texts = chunks

        # BM25 setup
        self.tokenized_chunks = [chunk.split() for chunk in chunks]
        self.bm25 = BM25Okapi(self.tokenized_chunks)

    # ---------------------------
    # Hybrid Query
    # ---------------------------
    def query(self, query, k=4, alpha=0.5):
        # ----- Dense Retrieval -----
        q_vec = embed_text([query])
        D, I = self.index.search(np.array(q_vec).astype("float32"), k * 2)

        dense_results = [
            (self.texts[i], D[0][idx])
            for idx, i in enumerate(I[0])
        ]

        # ----- BM25 Retrieval -----
        tokenized_query = query.split()
        bm25_scores = self.bm25.get_scores(tokenized_query)

        bm25_results = sorted(
            list(zip(self.texts, bm25_scores)),
            key=lambda x: x[1],
            reverse=True
        )[:k * 2]

        # ----- Normalize Scores -----
        def normalize(scores):
            min_s = min(scores)
            max_s = max(scores)
            return [(s - min_s) / (max_s - min_s + 1e-8) for s in scores]

        dense_norm = normalize([d for _, d in dense_results])
        bm25_norm = normalize([b for _, b in bm25_results])

        # ----- Combine Scores -----
        combined = {}

        # Dense contribution
        for i, (text, _) in enumerate(dense_results):
            combined[text] = alpha * dense_norm[i]

        # BM25 contribution
        for i, (text, _) in enumerate(bm25_results):
            combined[text] = combined.get(text, 0) + (1 - alpha) * bm25_norm[i]

        # ----- Final Ranking -----
        ranked = sorted(combined.items(), key=lambda x: x[1], reverse=True)

        return [text for text, _ in ranked[:k]]