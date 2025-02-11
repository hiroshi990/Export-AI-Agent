import asyncio
import nest_asyncio
nest_asyncio.apply()
import os
from langchain.agents import Tool,create_react_agent,AgentExecutor
from Document_sources import main,DocumentSources
from langchain_chroma import Chroma #type: ignore
from embeddings import EmbeddingStore
from prompts import prompt
from llm import GroqLLM

class compiler:
    def __init__(self,pdf_directory,url):
        self.pdf_directory=pdf_directory
        self.url=url
        self.doc_sources=DocumentSources(self.pdf_directory,self.url)
        pass
    def return_agent(self):
        vectordb_path=os.path.join(os.getcwd(),"vectordb")
        self.vector_store=EmbeddingStore()

        if not os.path.exists(vectordb_path):
            print("=== Initiating ===")
            print("=== Loading Documents ===")
            
            self.chunks, self.web_chunks = asyncio.run(main(self.pdf_directory,self.url))
            
            print("Number of pdf chunks:", len(self.chunks))
            print("Number of web chunks:", len(self.web_chunks))
            print("=== documents loaded ===")
            
            self.chunks.extend(self.web_chunks)
            print("Total number of chunks:", len(self.chunks))
        
            print("=== creating vectore store ===")
            self.vector_store_obj=self.vector_store.create_vector_store(self.chunks)
        else:
            self.vector_store_obj=Chroma(persist_directory="vectordb",embedding_function=self.vector_store.embedding_model)
        print("Number of embeddings:",self.vector_store_obj._collection.count())
        print("=== Vector Store Loaded ===")
        
        #setting up tools
        self.retriever = self.vector_store_obj.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        #modified retriever tool description
        self.retriever_tool = Tool(
            name="custom_retriever",
            func=self.retriever.get_relevant_documents,
            description="""Use this tool to retrieve information about export procedures,
            market trends, consumer preferences, and product details from the loaded documents.
            Input should be a specific question or topic."""
        )
        self.tavily_search = self.doc_sources.tavily_tool()
        print("=== tools created ===")
        self.tools=[self.retriever_tool, self.tavily_search]
        
        prompts=prompt()
        self.custom_prompt, self.memory=prompts.custom_prompt()
        
        print("=== Downloading LLM ===")
        self.llm_instance = GroqLLM()
        self.llm=self.llm_instance.llm_return()
        
        print("=== LLM downloaded ===")
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.custom_prompt
        ) 
        
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            memory=self.memory,
            max_iterations=20,
            max_execution_time=None,
            handle_parsing_errors=True,
            output_key="output",
            return_intermediate_steps=True
        )
        
        print("=== agent created ===")
        
        return self.agent_executor
    

if __name__ == "__main__":
    compiler()
    

        
        
    
