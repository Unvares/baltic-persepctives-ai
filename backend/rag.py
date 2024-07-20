import wikipedia
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from textwrap import wrap


def get_wikipedia_content(topic):
    for page in wikipedia.search(topic):
        try:
            return wrap(wikipedia.page(page).content, 512)
        except:
            pass


def get_retriever(topic):
    context = get_wikipedia_content(topic)
    if context is None:
        return None

    bge_m3_embeddings = HuggingFaceEndpointEmbeddings(model="https://bge-m3-embedding.llm.mylab.th-luebeck.dev")
    bge_m3 = Chroma.from_texts(context, bge_m3_embeddings, collection_name="bge_m3")
    retriever = bge_m3.as_retriever(search_kwargs={'k': 3})
    return retriever


if __name__ == '__main__':
    docs = get_retriever('TJEOIGDKLVNFCLKGM;LDF,GDGHF').invoke("When did strike happened?")
    for doc in docs:
        print("---")
        print(len(doc.page_content))
        print(doc.page_content)