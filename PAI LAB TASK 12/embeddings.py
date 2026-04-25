import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from data import qna_data

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

questions = [q for q, a in qna_data]
answers = [a for q, a in qna_data]

question_embeddings = model.encode(questions)

dim = question_embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(np.array(question_embeddings))

def search(query):
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), 3)

    results = []
    for i in I[0]:
        results.append((questions[i], answers[i]))
    return results