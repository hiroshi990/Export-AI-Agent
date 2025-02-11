import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq

groq_api=os.getenv("GROQ_API_KEY")

class GroqLLM:
    def __init__(self,model_name = "llama3-8b-8192"):
        self.model_name=model_name

    def llm_return(self):
        self.llm = ChatGroq(groq_api_key=groq_api,
                            model= self.model_name,temperature=0.1,
                            max_tokens=512)
        return self.llm
