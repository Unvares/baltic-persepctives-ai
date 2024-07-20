import os

from langchain_openai import ChatOpenAI


def get_model():
    api_key = "sk-proj-AdIuNRsaRBF521qXqYoST3BlbkFJBxgJ7H7mTT8u3uN9xmG5"
    # api_key = os.environ.get("API_KEY", "-")
    model = ChatOpenAI(streaming=True, api_key=api_key, model="gpt-4o-mini", max_tokens=100)
    return model
