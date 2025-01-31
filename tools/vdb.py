import faiss
from langchain_core.documents import Document
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


def get_documents(init_objects):
    documents = []
    for i in range(len(init_objects)):
      documents.append(Document(
          page_content=init_objects[i].text,
          metadata={"source": init_objects[i].url},
      ))
    return documents 

def get_document(text: str, url: str):
   return Document(page_content=text, metadata={"source": url} )

def config_vectors_storage():
   embeddings = OpenAIEmbeddings(
      model="text-embedding-3-small",
      openai_api_key="sk-KQvzzbKNqChegfWRcIrdwcr4SnM8s95Z",
      openai_api_base="https://api.proxyapi.ru/openai/v1"
      # With the `text-embedding-3` class
      # of models, you can specify the size
      # of the embeddings you want returned.
      # dimensions=1024
   )

   vector_len = 1536;

   index = faiss.IndexFlatL2(vector_len)

   return FAISS(
      embedding_function=embeddings,
      index=index,
      docstore=InMemoryDocstore(),
      index_to_docstore_id={},
   )


def config_vectors_storage_push(storage, text: str, url: str):
   storage.add_documents([get_document(text, url)])


def search_context(storage, query: str):
   return storage.similarity_search_with_relevance_scores("В каком году Университет ИТМО был включён в число Национальных исследовательских университетов России?", k=3)