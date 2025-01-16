import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.document_loaders import ImageLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate

# Load Groq API key from environment variables
groq_api_key = os.getenv('GROQ_API_KEY')

# Initialize Groq client
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

# Function to load PDFs and images
def load_documents_and_images(pdf_directory, image_directory):
    # Load PDFs
    pdf_loader = PyPDFDirectoryLoader(pdf_directory)
    pdf_docs = pdf_loader.load()

    # Load images
    image_loader = ImageLoader(image_directory)
    image_docs = image_loader.load()

    return pdf_docs, image_docs

# Function to process documents and create embeddings
def process_documents(pdf_docs, image_docs):
    # Combine documents
    all_docs = pdf_docs + image_docs

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_documents = text_splitter.split_documents(all_docs)

    # Create FAISS vector store
    vector_store = FAISS.from_documents(final_documents)

    return vector_store

# Example usage
pdf_directory = "./path_to_pdfs"
image_directory = "./path_to_images"
pdf_docs, image_docs = load_documents_and_images(pdf_directory, image_directory)
vector_store = process_documents(pdf_docs, image_docs)

# Define a prompt template for querying
prompt_template = PromptTemplate(template="Answer the following question based on the context: {context}\nQuestion: {question}")

# Example query
query = "What is depicted in the uploaded images?"
response = llm.invoke({"context": vector_store, "question": query})

print(response)

"""
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings

# Create the vector store
vector_store = MongoDBAtlasVectorSearch.from_connection_string(
   connection_string = ATLAS_CONNECTION_STRING,
   embedding = OpenAIEmbeddings(disallowed_special=()),
   namespace = "sample_mflix.embedded_movies",
   text_key = "plot",
   embedding_key = "plot_embedding",
   relevance_score_fn = "dotProduct"
)

vector_store.create_vector_search_index(
   dimensions = 1536
)

from langchain_mongodb.index import create_fulltext_search_index
from pymongo import MongoClient

# Connect to your cluster
client = MongoClient(ATLAS_CONNECTION_STRING)

# Use helper method to create the search index
create_fulltext_search_index(
   collection = client["sample_mflix"]["embedded_movies"],
   field = "plot",
   index_name = "search_index"
)

from langchain_mongodb.retrievers.hybrid_search import MongoDBAtlasHybridSearchRetriever

# Initialize the retriever
retriever = MongoDBAtlasHybridSearchRetriever(
    vectorstore = vector_store,
    search_index_name = "search_index",
    top_k = 5,
    fulltext_penalty = 50,
    vector_penalty = 50
)

# Define your query
query = "time travel"

# Print results
documents = retriever.invoke(query)
for doc in documents:
   print("Title: " + doc.metadata["title"])
   print("Plot: " + doc.page_content)
   print("Search score: {}".format(doc.metadata["fulltext_score"]))
   print("Vector Search score: {}".format(doc.metadata["vector_score"]))
   print("Total score: {}\n".format(doc.metadata["fulltext_score"] + doc.metadata["vector_score"]))


"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import  RunnablePassthrough
from langchain_openai import ChatOpenAI

# Define a prompt template
template = """
   Use the following pieces of context to answer the question at the end.
   {context}
   Question: Can you recommend some movies about {query}?
"""
prompt = PromptTemplate.from_template(template)
model = ChatOpenAI()

# Construct a chain to answer questions on your data
chain = (
   {"context": retriever, "query": RunnablePassthrough()}
   | prompt
   | model
   | StrOutputParser()
)

# Prompt the chain
query = "time travel"
answer = chain.invoke(query)
print(answer)