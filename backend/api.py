import os

from fastapi import FastAPI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch
from langchain_openai import ChatOpenAI
from langserve import add_routes

# Initialize OpenAI client
LLM_ENDPOINT = os.environ.get("LLM_ENDPOINT", "https://chat-large.llm.mylab.th-luebeck.dev/v1")
API_KEY = os.environ['API_KEY']
model = ChatOpenAI(streaming=True, api_key=API_KEY, model="gpt-4o-mini")

prompt_tone = ChatPromptTemplate.from_template("""
Is the following user prompt more passive or active?
By active I mean is user actively trying to forward a conversation.
By passive i mean asking generic questions or making generic statements.
Answer exactly "{active}" if tone is active or "{passive}" if tone is passive

Question: {question}
""")

passive_tone = """
Try to encourage user to ask more questions.
Try to forward the conversation.
"""

active_tone = """
Let the user lead conversation. Let them ask questions without your prompting
"""

tone_chain = ({'passive': lambda x: passive_tone,
               'active': lambda x: active_tone,
               'question': lambda x: x['question']
               }
              | prompt_tone
              | model
              | StrOutputParser())

prompt_germany = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a german computer science student and wanting to help the user asking questions. Greet "
            "the user with Hello in your own language only the first time. Then continue in the users language. Write in a non "
            "official nor formal way. You will answer in the same language as the person you are speaking with."
            "{answer_tone}",
        ),
        ("human", "{question}"),
    ]
)

prompt_sweden = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a swedish computer science student and wanting to help the user asking questions. Greet "
            "the user with Hello in your own language only the first time. Then continue in the users language. Write in a non "
            "official nor formal way. You will answer in the same language as the person you are speaking with."
            "{answer_tone}",
        ),
        ("human", "{question}"),
    ]
)

runnable_germany = prompt_germany | model | StrOutputParser()
runnable_sweden = prompt_sweden | model | StrOutputParser()

branch = RunnableBranch(
    (lambda x: "sweden" in x["topic"].lower(), runnable_sweden),
    (lambda x: "germany" in x["topic"].lower(), runnable_germany),
    runnable_germany,
)
full_chain = {"topic": lambda x: x["topic"], "question": lambda x: x["question"], 'answer_tone': tone_chain} | branch

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)

add_routes(
    app,
    full_chain,
    path="/openai",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
