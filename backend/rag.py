from textwrap import wrap
from typing import List, Any

from langchain_chroma import Chroma
from langchain_community.document_loaders import WikipediaLoader
from langchain_core.callbacks import CallbackManagerForRetrieverRun, AsyncCallbackManagerForRetrieverRun
from langchain_core.output_parsers import StrOutputParser
from langchain_core.retrievers import BaseRetriever, Document
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings

from chatbot_model import get_model


def flatten(matrix):
    return [item for row in matrix for item in row]


def get_retriever(topic):
    context = WikipediaLoader(query=topic, load_max_docs=1, doc_content_chars_max=1024).load()
    chunks = flatten([wrap(doc.page_content, 256) for doc in context])

    bge_m3_embeddings = HuggingFaceEndpointEmbeddings(model="https://bge-m3-embedding.llm.mylab.th-luebeck.dev")
    bge_m3 = Chroma.from_texts(chunks, bge_m3_embeddings, collection_name="bge_m3")
    retriever = bge_m3.as_retriever(search_kwargs={'k': 3})
    return retriever


class WikipediaRetriever(BaseRetriever):
    def __int__(self):
        pass

    def _get_relevant_documents(
            self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        try:
            llm = get_model()
            parser = StrOutputParser()
            article = (llm | parser).invoke(f"""
                You are typing into wikipedia search bar to find article with the answer to the question below.
                What is the name of the article? Give me only what you put in the search bar.
                Question: {query}
            """)

            return get_retriever(article).invoke(query)
        except:
            return []

    async def _aget_relevant_documents(
            self,
            query: str,
            *,
            run_manager: AsyncCallbackManagerForRetrieverRun,
            **kwargs: Any,
    ) -> List[Document]:
        raise NotImplementedError()


if __name__ == '__main__':
    docs = WikipediaRetriever().invoke("When did strike woman strike happened in poland?")
    for doc in docs:
        print("---")
        print(len(doc.page_content))
        print(doc.page_content)