import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFDirectoryLoader
#from langchain_community.document_loaders import ImageLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
#from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
#from langchain_mongodb.index import create_fulltext_search_index
from pymongo import MongoClient
#from langchain_mongodb.retrievers.hybrid_search import MongoDBAtlasHybridSearchRetriever

load_dotenv()
# Load Groq API key from environment variables
groq_api_key = os.getenv('GROQ_API_KEY')
gemini_api_key = os.getenv('GEMINI_API_KEY')
atlas_connection_string = os.getenv('ATLAS_CONNECTION_STRING')
tracing_v2=os.getenv("LANGCHAIN_TRACING_V2")
langchain_api_key=os.getenv("LANGCHAIN_API_KEY")

# Initialize Groq client
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")
embeddings = GoogleGenerativeAIEmbeddings(google_api_key=gemini_api_key, model="models/embedding-001")
client = MongoClient(atlas_connection_string)

DB_NAME = "langchain_test_db"
COLLECTION_NAME = "langchain_test_vectorstores"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "langchain-test-index-vectorstores"

MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

vector_store = MongoDBAtlasVectorSearch(
    collection=MONGODB_COLLECTION,
    embedding=embeddings,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn="cosine",
)

# Create vector search index on the collection
# Since we are using the default OpenAI embedding model (ada-v2) we need to specify the dimensions as 1536
#vector_store.create_vector_search_index(dimensions=768)
# Function to load PDFs and images
def load_documents_and_images(pdf_directory):
    # Load PDFs
    pdf_loader = PyPDFDirectoryLoader(pdf_directory)
    print(pdf_loader)
    pdf_docs = pdf_loader.load()

    return pdf_docs

# Function to process documents and create embeddings
def process_documents(pdf_docs):
    # Combine documents
    all_docs = pdf_docs

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_documents = text_splitter.split_documents(all_docs)

    vector_store.add_documents(documents=final_documents)#, ids=uuids)

# Example usage
pdf_directory = os.getenv('FILE_PATH')

pdf_docs = load_documents_and_images(pdf_directory=pdf_directory)
print(pdf_docs)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
final_documents = text_splitter.split_documents(pdf_docs)

vector_store.add_documents(documents=final_documents)

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

prompt=ChatPromptTemplate.from_template("""
                    You are a university professer. 
                    Your role is to correct and evaluation students' answer paper. 
                    You will receive university answer sheet & evaluation metrics to help you evaluate the papers. 
                    You will be rewarded generously for doing a great evaluation.
                    <context>
                    {context}
                    </context>
                    Question: {input}
            """)

# Construct a chain to answer questions on your data
document_chain = create_stuff_documents_chain(llm, prompt)
retriever = vector_store.as_retriever()
#    search_type="similarity_score_threshold",
#    search_kwargs={"k": 1, "score_threshold": 0.2},
#)
retrieval_chain = create_retrieval_chain(
                            retriever,
                            document_chain,
                        )

# Prompt the chain
query = "Can you print all the text in your given context"
retrieval_chain.invoke({"input": query})
#print(answer)

print("DOne")