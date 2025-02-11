from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma # type: ignore
import torch # type: ignore
torch.classes.__path__ = []  

class EmbeddingStore:
    def __init__(self,embedding_model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.embedding_model=HuggingFaceEmbeddings(model_name=embedding_model_name)
        self.vector_store=None

    def create_vector_store(self,documents):
        self.vector_store=Chroma.from_documents(documents=documents,embedding=self.embedding_model,
                                                persist_directory="vectordb")
        return self.vector_store
    

