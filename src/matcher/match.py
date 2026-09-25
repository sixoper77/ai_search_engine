import os

os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"


import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.cross_encoder import CrossEncoder
from sentence_transformers.util import cos_sim

from src.search.schemas import Source

embedder = SentenceTransformer("intfloat/multilingual-e5-small")
reranker = CrossEncoder("BAAI/bge-reranker-v2-m3")
BI_ENCODER_TOP_K = 30


def match_results(query: str, corpus: list[Source]) -> list[Source]:
    if len(corpus) == 0:
        raise ValueError("The text corpus is empty.")
    corpus = list(dict.fromkeys(corpus))
    formatted_query = f"query: {query}"
    formatted_corpus = [f"passage: {doc.text}" for doc in corpus]

    query_embedding = embedder.encode(formatted_query, convert_to_tensor=True)
    corpus_embeddings = embedder.encode(formatted_corpus, convert_to_tensor=True)

    similarity_scores = cos_sim(query_embedding, corpus_embeddings)[0]
    top_k = min(BI_ENCODER_TOP_K, len(corpus))
    bi_scores, indieces = torch.topk(similarity_scores, top_k)

    cross_inp = [[query, corpus[idx].text] for idx in indieces]
    cross_scores = reranker.predict(cross_inp)
    results = []
    for bi_score, cross_score, idx in zip(bi_scores, cross_scores, indieces):
        results.append(
            {
                "text": corpus[idx].text,
                "url": corpus[idx].url,
                "bi_score": bi_score.item(),
                "cross_score": cross_score.item(),
            }
        )
    results = sorted(results, key=lambda x: x["cross_score"], reverse=True)
    text_results = [Source(text=res["text"], url=res["url"]) for res in results[:12]]
    print(text_results)
    print(len(text_results))
    return text_results
