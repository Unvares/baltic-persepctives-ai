import os
import re
from pathlib import Path
from typing import Any, Callable, Dict, Union

from fastapi import FastAPI, HTTPException, Request
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core import __version__
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.runnables import RunnableBranch
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langserve import add_routes
from starlette.middleware.cors import CORSMiddleware
from typing_extensions import TypedDict

from language_chain import language_chain
from topic_chain import branch
from tone_chain import tone_chain
from history_chain import chain_with_history
from chatbot_model import get_model

# Initialize OpenAI client
model = get_model()


def _per_request_config_modifier(
    config: Dict[str, Any], request: Request
) -> Dict[str, Any]:
    """Update the config"""
    config = config.copy()
    configurable = config.get("configurable", {})


    if configurable['user_id'] is None:
        raise HTTPException(
            status_code=400,
            detail="No user id found. Please set a cookie named 'user_id'.",
        )
    
    config['configurable'] = configurable

    # configurable["user_id"] = user_id
    # config["configurable"] = configurable
    return config


full_chain = {"topic": lambda x: x["topic"], "question": lambda x: x["question"],
              'answer_tone': tone_chain, 'character': branch,  'new_topic': lambda x: get_persona_chain(x['question'])[:3].lower(), 'language': language_chain} | chain_with_history

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

add_routes(
    app,
    full_chain,
    per_req_config_modifier=_per_request_config_modifier,
    path="/openai",
    disabled_endpoints=["playground", "batch"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
