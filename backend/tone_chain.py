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
from langchain_core.runnables import ConfigurableFieldSpec, RunnablePassthrough
from langchain_core.runnables import RunnableBranch
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langserve import add_routes
from starlette.middleware.cors import CORSMiddleware
from typing_extensions import TypedDict

from chatbot_model import get_model
from history_chain import chain_with_history

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

model = get_model()
tone_chain = ({'passive': lambda x: passive_tone,
               'active': lambda x: active_tone,
               'question': lambda x: x['question']
               }
              | prompt_tone
              | model
              | StrOutputParser()
              )
