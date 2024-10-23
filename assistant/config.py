from typing import Optional
class Config():
    """Config class for customizing the Babylon Assistant
    grade_level : the grade_level of the student that will be using the chatbot, (1 - 12)
    retrieval_type : where you want your retrieval information to be stored (db)
    model_name : name of the LLM model to use
    rerank : boolean to describe whether or not to use rerank queries
    rag_model : describes which rag technique to use
    hyde : boolean to turn on hybrid search or not
    context_length : length of the context chat window
    """
    def __init__(self, grade_level : int = 4, retrieval_type : str = "db", model_name : str = "gpt-4-turbo", rerank : bool = False,
                 rag_model : str = "dense_search", hyde : bool = False, context_length : int = 1000
                 ):
        self.grade_level = grade_level
        self.retrieval_type = retrieval_type
        self.model_name = model_name
        self.rerank = rerank
        self.context_length = None
        self.hyde = False # bool
        self.rag_model = rag_model
