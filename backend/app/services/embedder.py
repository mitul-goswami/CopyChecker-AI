from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_mongodb.index import create_fulltext_search_index
from pymongo import MongoClient

class Vectorize():
    def __init__(self):
        self.pdf_text = None
        self.pdf_image = None
        load_dotenv() #dont commit
        self.__google_api_key = os.getenv("GEMINI_API_KEY")
        self.__atlas_key = os.getenv("ATLAS_CONNECTION_STRING")
        self.__db_name = os.getenv("DB_NAME")
        self.__collection_name = os.getenv("COLLECTION_NAME")
        self.__vector_name = os.getenv("VECTOR_INDEX")
        self.__keyword_name = os.getenv("KEYWORD_INDEX")
    def client_setup(self):
        collection = None
        client = MongoClient(self.__atlas_key)
        database = client[self.__db_name]
        collection_list = database.list_collections()
        if self.__collection_name not in collection_list:
            collection = database[self.__collection_name]
        results = list(collection.list_search_indexes())
        if (self.__vector_name not in results) and (self.__keyword_name not in results):
            if (self.__vector_name not in results):
                embeddings = GoogleGenerativeAIEmbeddings(google_api_key=self.__google_api_key, model="models/embedding-001")
                vector_store = MongoDBAtlasVectorSearch(
                    collection=collection,
                    embedding=embeddings,
                    index_name=self.__vector_name,
                    relevance_score_fn="cosine",
                )
                vector_store.create_vector_search_index(dimensions=768)
            if (self.__keyword_name not in results):
                create_fulltext_search_index(
                    collection = collection,
                    field = "plot",
                    index_name = self.__keyword_name
                )
    def chunker(self, pdf):
        docs = pdf["text"]

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=250, chunk_overlap=0
        )

        self.pdf_text = text_splitter.split_documents(docs)
    def store(self, pdf):
        try:
            embeddings = GoogleGenerativeAIEmbeddings(google_api_key=self.__google_api_key, model="models/embedding-001")
            client = MongoClient(self.__atlas_key)
            collection = client[self.__db_name][self.__collection_name]
            vector_store = MongoDBAtlasVectorSearch(
                collection=collection,
                embedding=embeddings,
                index_name=self.__vector_name,
                relevance_score_fn="cosine",
            )
            self.pdf_image = pdf["image"]
            texts = [doc for doc in self.pdf_text]
            vector_store.add_documents(texts)
            vector_store.add_documents(self.pdf_image)
            return True
        except Exception as e:
            raise e
        #print("Storage Done")