from glob import glob
import requests
import zipfile
import io
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from langchain_chroma import Chroma

EMBEDDING_EP = os.environ.get("EMBEDDING_EP", "https://bge-m3-embedding.llm.mylab.th-luebeck.dev/")

embeddings = HuggingFaceEndpointEmbeddings(model="https://bge-m3-embedding.llm.mylab.th-luebeck.dev")

print("Downloading prompt engineering guide")
url = 'https://github.com/dair-ai/Prompt-Engineering-Guide/archive/refs/heads/main.zip'
response = requests.get(url)
with zipfile.ZipFile(io.BytesIO(response.content)) as the_zip_file:
    the_zip_file.extractall('/data') 

text_splitter = text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)

texts = list(glob("/data/Prompt-Engineering-Guide-main/ar-pages/**/*.ar.mdx"))
chunks = []

for doc in texts:
    with open(doc) as f:
        for chunk in text_splitter.split_text(f.read()):
            try:
                chunks.append(chunk)
            except Exception as ex:
                print(doc, len(chunk), "not processable", str(ex))

print("Generate semantic index for prompt engineering guide")
vectorstore = Chroma.from_texts(chunks, embeddings, persist_directory="/data")
