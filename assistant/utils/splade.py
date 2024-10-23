"""SPLADE embeddings (sparse), unfinished and not fully functional"""
import torch
from langchain_core.documents.base import Document
import numpy as np
from transformers import AutoModelForMaskedLM, AutoTokenizer
from typing import List
import os
import pickle
import scipy

class SPLADEEmbeddings():
    def __init__(self, model_id : str = 'naver/splade-cocondenser-ensembledistil'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForMaskedLM.from_pretrained(model_id)
        self._embeddings = None
        self._l2_norm_matrix = None
        self._ids = None
        self._documents = None
        self.embeddings_path = os.getcwd()
    def string_to_embedding(self, inputs : List[str]):
        tokens = self.tokenizer(inputs, return_tensors="pt", padding=True, truncation=True)
        output = self.model(**tokens)
        vecs = (
            torch.max(
                torch.log(1 + torch.relu(output.logits))
                * tokens.attention_mask.unsqueeze(-1),
                dim=1,
            )[0]
            .squeeze()
            .detach()
            .cpu()
            .numpy()
        )
        return vecs
    def add_embeddings(self, new_docs : List[Document]):
        if self._embeddings is None or self._ids is None:
            self.load()
        embeddings, ids = self.generate_embeddings_from_docs(
            docs=new_docs, keep=True
        )
        if self._ids is not None and self._embeddings is not None:
            updated_embeddings = np.vstack((self._embeddings.toarray(), embeddings))
            updated_ids = self._ids.tolist() + ids
            self.persist_embeddings(updated_embeddings, updated_ids)
        else:
            raise Exception(
                "Something is wrong: ids and embeddings weren't loaded properly."
            )

    def generate_embeddings_from_docs(self, docs : List[Document], keep : bool = True):
        texts = [d.page_content for d in docs]
        ids = [d.metadata["document_id"] for d in docs]
        vecs = self.string_to_embedding(texts)
        embeddings = np.vstack(vecs)
        if keep:
            self.persist_embeddings(embeddings, ids, docs)
        return embeddings, ids
    def persist_embeddings(self, embeddings, ids, documents):
        folder_path, embeddings_path, fn_ids, fn_documents = self._get_embedding_fnames()
        csr_embeddings = scipy.sparse.csr_matrix(embeddings)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        scipy.sparse.save_npz(embeddings_path, csr_embeddings)
        self.save_list(ids, fn_ids)
        self.save_list(documents, fn_documents)
    def load(self):
        _, embeddings_path, fn_ids, fn_documents= self._get_embedding_fnames()
        try:
            self._embeddings = scipy.sparse.load_npz(embeddings_path)
            self._l2_norm_matrix = scipy.sparse.linalg.norm(self._embeddings, axis=1)
            with open(fn_ids, "rb") as fp:
                self._ids = np.array(pickle.load(fp))
            with open(fn_documents, "rb") as fp:
                self._documents = pickle.load(fp)
        except FileNotFoundError:
            raise FileNotFoundError(
                "Embeddings don't exist, run generate_embeddings_from_docs(..) first."
            )
    def _get_embedding_fnames(self):
        folder_name = os.path.join(self.embeddings_path, "splade")
        fn_embeddings = os.path.join(folder_name, "splade_embeddings.npz")
        fn_ids = os.path.join(folder_name, "splade_ids.pickle")
        fn_documents = os.path.join(folder_name, "splade_documents.pickle")
        return folder_name, fn_embeddings, fn_ids, fn_documents
    def search(self, top_k : int, query : str):
        if self._embeddings is None:
            self.load()
        #TODO: add label searching
        l2_norm_matrix = scipy.sparse.linalg.norm(self._embeddings, axis=1)
        query_embedding = self.string_to_embedding(inputs=[query])
        l2_norm_query = scipy.linalg.norm(query_embedding)
        cosine_similarity = self._embeddings.dot(query_embedding) / (
                l2_norm_matrix * l2_norm_query
            )
            # print(cosine_similarity)
        most_similar = np.argsort(cosine_similarity)
        top_similar_indices = most_similar[-top_k:][::-1]
        doc_ids : List[Document] = self._ids[top_similar_indices]
        return_docs = []
        for id in doc_ids:
            for doc in self._documents:
                if doc.metadata["document_id"] in doc_ids:
                    return_docs.append(doc.page_content)
        return return_docs
        # return (cosine_similarity[top_similar_indices], self._ids[top_similar_indices])
    # def find_docs(self, ids):
    #     for id in ids:

    def save_list(self, list_: list, fname: str) -> None:
        # store list in binary file so 'wb' mode
        with open(fname, "wb") as fp:
            pickle.dump(list_, fp)