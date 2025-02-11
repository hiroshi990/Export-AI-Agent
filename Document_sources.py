from dotenv import load_dotenv
load_dotenv()
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_community.tools import TavilySearchResults
import re
from bs4 import BeautifulSoup
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, RecursiveUrlLoader
import asyncio
import os
import nest_asyncio
nest_asyncio.apply()
from groq import Groq
import torch

tavily_api=os.getenv("TAVILY_API_KEY")

class DocumentSources:
  def __init__(self,directory_path,urls,exclude_urls:list = None):
    self.urls=urls
    self.exclude_urls=exclude_urls
    self.directory_path=directory_path

  def extractor(self,input: str) -> str:
    """Extracts and cleans text content from HTML."""
    soup = BeautifulSoup(input, "lxml")

    # Remove script, style and footer elements
    for rm_elements in soup.find(["script", "style","footer"]):
      if rm_elements:
        rm_elements.decompose()

    # removing the partnersup div class
    partnersup_div = soup.find("div", class_="container-xl")
    if partnersup_div:
      partnersup_div.decompose()
    else:
      print("Partnersup div not found")
      
    # remove the main_header div class
    main_header_div=soup.find("div",class_="mainHeader")
    if main_header_div:
      main_header_div.decompose()
    else:
      print("main header div not found")
      
    # Extract text and clean it
    raw_text = soup.get_text(separator="\n")
    cleaned_text = re.sub(r"\s{2,}", " ", raw_text)  
    cleaned_text = re.sub(r"\n{2,}", " ", cleaned_text) 
    return cleaned_text.strip()

  # creating the loading function
  async def web_loader(self):
    if self.exclude_urls is None:
      web_loader = RecursiveUrlLoader(url = self.urls,max_depth=2,
                                      use_async=True,
                                      extractor=self.extractor)
    else:
      web_loader = RecursiveUrlLoader(url = self.urls,max_depth=2,
                                      use_async=True,
                                      exclude_dirs=self.exclude_urls,
                                      extractor=self.extractor)

    web_documents=web_loader.load()
    
    print(f"loaded {len(web_documents)} documents from {self.urls}")

    return web_documents



  async def load_documents(self):
    #load documents from directory
    loader=DirectoryLoader(self.directory_path,glob="**/*.pdf",loader_cls=PyPDFLoader,
                          show_progress=True)
    documents=loader.load()

    #split documents
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    pdf_chunks=text_splitter.split_documents(documents)
    print(f"loaded {len(documents)} documents from {self.directory_path}")
    return pdf_chunks

  def tavily_tool(self,api=tavily_api):
    search = TavilySearchAPIWrapper(tavily_api_key=api)
    tavily_tool = TavilySearchResults(api_wrapper=search,
                                      max_results=1,
                                      include_raw_content=False)
    print("tavily tool created")
    return tavily_tool


async def main(path,url):
  # Create a DocumentSources instance only once to avoid potential issues
  doc_sources = DocumentSources(path, url)
  chunks=await asyncio.create_task(doc_sources.load_documents())
  web_chunks=await asyncio.create_task(doc_sources.web_loader())
  return (chunks,
          web_chunks)
