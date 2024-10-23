"""HuggingFace CrossEncoderRanker used in reranking"""

from typing import List
from langchain_core.documents.base import Document
from sentence_transformers.cross_encoder import CrossEncoder

class CrossEncoderRanker():
    "Simple Cross Encoder Reranker, not using LLM's"
    def __init__(self, cross_encoder_name : str):
        self.encoder_name = cross_encoder_name
        self.model = CrossEncoder(cross_encoder_name)
    def get_scores(self, query : str, docs : List[Document]) -> List[float]:
        features = [[query, x.page_content] for x in docs]
        scores = self.model.predict(features).tolist()
        return scores
    def rerank(self, query: str, docs : List[Document]):
        scores = self.get_scores(query, docs)
        scores_with_docs = {scores[i] : docs[i] for i in range(len(scores))}
        keys = list(scores_with_docs.keys())
        keys.sort(reverse=True)
        final = [scores_with_docs[x] for x in keys]
        return final
    def preferred_answer(self, answer1 : str, answer2 : str, query : str) -> str:
        answers = [answer1, answer2]
        features = [[query, x] for x in answers]
        scores = self.model.predict(features).tolist()
        if scores[0] > scores[1]:
            return answer1
        return answer2