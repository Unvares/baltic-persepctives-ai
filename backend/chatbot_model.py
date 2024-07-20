import os

from langchain_openai import ChatOpenAI


def get_model():
    api_key = os.environ.get("API_KEY", "-")
    model = ChatOpenAI(
        streaming=True, api_key=api_key, model="gpt-4o-mini"
    )
    return model
