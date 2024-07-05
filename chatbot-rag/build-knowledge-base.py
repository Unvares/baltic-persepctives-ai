from glob import glob
import requests
import zipfile
import io

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

embeddings = OpenAIEmbeddings(api_key="sk-proj-M0N3AniQmJwCGttxwUn5T3BlbkFJ6VhsTuPbdauF8WeMrxRv")

print("Downloading prompt engineering guide")
url = 'https://github.com/dair-ai/Prompt-Engineering-Guide/archive/refs/heads/main.zip'
response = requests.get(url)
with zipfile.ZipFile(io.BytesIO(response.content)) as the_zip_file:
    the_zip_file.extractall('/data') 

text_splitter = text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=3000,
    chunk_overlap=500,
    length_function=len,
    is_separator_regex=False,
)

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
