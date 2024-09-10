import os
import tiktoken

from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings

from langchain_ollama import ChatOllama

tiktoken_cache_dir = ''
os.environ["TIKTOKEN_CACHE_DIR"] = tiktoken_cache_dir

assert os.path.exists(os.path.join(tiktoken_cache_dir, "9b5ad71b2ce5302211f9c61530b329a4922fc6a4"))

tokenizer = tiktoken.get_encoding("cl100k_base")

def tiktoken_len(text):
    tokens = tokenizer.encode(text)
    return len(tokens)

llm = ChatOllama(
    model = "EEVE-Korea-10.8b"
)

loader = PyPDFLoader("")
pages = loader.load_and_split()

text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50, length_function = tiktoken_len)
texts = text_splitter.split_documents(pages)

model_kwargs = {"device": 'cpu'}
encode_kwargs = {'normalize_embeddings': True}

ko = HuggingFaceEmbeddings(
    model_name = ''
    model_kwargs = model_kwargs
    encode_kwargs = encode_kwargs
)

dosearch = Chroma.from_documents(texts, ko)
qa = RetrievalQA(llm = llm,
                    chain_type = 'stuff'
                    retriever = dosearch.as_retriever(
                        search_type = 'mmr',
                        search_kwargs={'k':3, 'fetch_k':10}),
                    return_source_documents = True
                    
)

def get_answer(message):
    return qa(message)
