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
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langserve import add_routes
from starlette.middleware.cors import CORSMiddleware
from typing_extensions import TypedDict
from personas import PERSONAS


def create_persona_chain(country):
    person_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f"{PERSONAS[country]}"
            "{answer_tone}",
        ),
        ("human", "{question}"),
    ])
    return person_prompt


branch = RunnableLambda(
    lambda x: create_persona_chain(x['topic']).lower()
)
