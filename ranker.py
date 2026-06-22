from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

def calculate_similarity_score(
    resume_text,
    jd_text
):

    resume_embedding = model.encode(
        resume_text
    )

    jd_embedding = model.encode(
        jd_text
    )

    similarity = cosine_similarity(
        [resume_embedding],
        [jd_embedding]
    )[0][0]

    return round(similarity * 100)