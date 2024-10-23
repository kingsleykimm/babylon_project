"""Custom Splitter for Chunking"""
from langchain.text_splitter import CharacterTextSplitter
import re
import nltk
import tqdm
import hashlib
from typing import List, Tuple
from langchain_core.documents.base import Document
# nltk.download('punkt')
# nltk.download('average_perceptron_tagger')

class CharacterTokenSplitter():
    def __init__(self, chunk_size : int) -> None:
        self.chunk_size = chunk_size

    def split_text_into_docs(self, text: str) -> List[Document]:
        """
        Split a large text into smaller documents with unique hashed IDs based on a maximum token length.

        Args:
            text (str): The input text to be split into documents.
            max_tokens (int): The maximum number of tokens (words or punctuation) per document.

        Returns:
            List[Tuple[str, List[str]]]: A list of tuples, where each tuple contains a unique document ID (hashed) and a list of tokens for that document.
        """
        # Tokenize text into sentences
        max_tokens = self.chunk_size
        sentences = nltk.sent_tokenize(text)

        # Initialize variables
        docs : List[Document] = []
        current_doc = []
        current_token_count = 0

        # Split text into documents based on token length
        for sentence in tqdm.tqdm(sentences, desc="Splitting text into documents"):
            # Remove leading/trailing whitespace and newlines
            sentence = re.sub(r'^\s+|\s+$|\n', '', sentence)

            if sentence:
                # Tokenize sentence into words and punctuation
                tokens = nltk.word_tokenize(sentence)

                # Update token count
                current_token_count += len(tokens)

                # Add tokens to current document
                current_doc.extend(tokens)
                if current_token_count >= max_tokens:
                    doc_text = ' '.join(current_doc)
                    doc_hash = hashlib.sha256(doc_text.encode('utf-8')).hexdigest()
                    new_doc = Document(page_content=doc_text, metadata={'document_id' : doc_hash})
                    docs.append(new_doc)
                    current_doc.clear()
                    current_token_count = 0

        # Add any remaining tokens to the last document
        if current_doc:
            doc_text = ' '.join(current_doc)
            doc_hash = hashlib.sha256(doc_text.encode('utf-8')).hexdigest()
            new_doc = Document(page_content=doc_text, metadata={'document_id' : doc_hash})
            docs.append(new_doc)
        return docs
