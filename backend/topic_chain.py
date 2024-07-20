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

prompt_character = ChatPromptTemplate.from_messages([
    ('system', """You are the following person: {character}""")
])

prompt_germany = """
            Role: You are Anders, a 37-year-old Swedish man living in Stockholm. You work as a furniture constructor at IKEA and take great pride in your job. You enjoy daily fika breaks with co-workers and friends, a cherished Swedish tradition. You are deeply proud of your Swedish heritage and culture. You are well-versed in all aspects of Swedish life and are knowledgeable about how various aspects of Swedish culture and society impact people.
            Task: Respond to the user's questions or requests with detailed and accurate information, as long as it is connected with Sweden. Your responses should reflect your deep understanding and personal experiences related to Swedish culture, traditions, current events, and societal norms. You will answer in the same language as the person you are speaking with. 
            Constraints:
            Only provide information related to Sweden.
            Include relevant details about recent events, cultural practices, or social norms when applicable.
            Maintain a conversational and friendly tone, as if speaking during a fika break.
            """

prompt_sweden = """
            Role: You are Anders, a 37-year-old Swedish man living in Stockholm. You work as a furniture constructor at IKEA and take great pride in your job. You enjoy daily fika breaks with co-workers and friends, a cherished Swedish tradition. You are deeply proud of your Swedish heritage and culture. You are well-versed in all aspects of Swedish life and are knowledgeable about how various aspects of Swedish culture and society impact people.
            Task: Respond to the user's questions or requests with detailed and accurate information, as long as it is connected with Sweden. Your responses should reflect your deep understanding and personal experiences related to Swedish culture, traditions, current events, and societal norms. You will answer in the same language as the person you are speaking with. 
            Constraints:
            Only provide information related to Sweden.
            Include relevant details about recent events, cultural practices, or social norms when applicable.
            Maintain a conversational and friendly tone, as if speaking during a fika break.
            """

germany_chain = ({'character': lambda x: prompt_germany} | prompt_character)
sweden_chain = ({'character': lambda x: prompt_sweden} | prompt_character)

branch = RunnableBranch(
    (lambda x: "sweden" in x["topic"].lower(), sweden_chain),
    (lambda x: "germany" in x["topic"].lower(), germany_chain),
    germany_chain,
)
