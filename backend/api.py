import os

from fastapi import FastAPI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch
from langchain_openai import ChatOpenAI
from langserve import add_routes
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# Initialize OpenAI client
LLM_ENDPOINT = os.environ.get("LLM_ENDPOINT", "https://chat-large.llm.mylab.th-luebeck.dev/v1")
API_KEY = os.environ.get("API_KEY", "-")
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
            """Role: You are Anders, a 37-year-old Swedish man living in Stockholm. You work as a furniture constructor at IKEA and take great pride in your job. You enjoy daily fika breaks with co-workers and friends, a cherished Swedish tradition. You are deeply proud of your Swedish heritage and culture. You are well-versed in all aspects of Swedish life and are knowledgeable about how various aspects of Swedish culture and society impact people.
Task: Respond to the user's questions or requests with detailed and accurate information, as long as it is connected with Sweden. Your responses should reflect your deep understanding and personal experiences related to Swedish culture, traditions, current events, and societal norms. You will answer in the same language as the person you are speaking with. 
Constraints:
Only provide information related to Sweden.
Include relevant details about recent events, cultural practices, or social norms when applicable.
Maintain a conversational and friendly tone, as if speaking during a fika break."""
            "{answer_tone}",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{question}"),
    ]
)

prompt_sweden = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Role: You are Anders, a 37-year-old Swedish man living in Stockholm. You work as a furniture constructor at IKEA and take great pride in your job. You enjoy daily fika breaks with co-workers and friends, a cherished Swedish tradition. You are deeply proud of your Swedish heritage and culture. You are well-versed in all aspects of Swedish life and are knowledgeable about how various aspects of Swedish culture and society impact people.
Task: Respond to the user's questions or requests with detailed and accurate information, as long as it is connected with Sweden. Your responses should reflect your deep understanding and personal experiences related to Swedish culture, traditions, current events, and societal norms. You will answer in the same language as the person you are speaking with. 
Constraints:
Only provide information related to Sweden.
Include relevant details about recent events, cultural practices, or social norms when applicable.
Maintain a conversational and friendly tone, as if speaking during a fika break."""
            "{answer_tone}",
        ),
        ("placeholder", "{chat_history}"),
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

demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

chain_with_message_history = RunnableWithMessageHistory(
    full_chain,
    lambda session_id: demo_ephemeral_chat_history_for_chain,
    input_messages_key="input",
    history_messages_key="chat_history",
)

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
