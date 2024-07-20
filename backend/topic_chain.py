import os
import re
from pathlib import Path
from typing import Any, Callable, Dict, Union

from fastapi import FastAPI, HTTPException, Request
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core import __version__
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langserve import add_routes
from starlette.middleware.cors import CORSMiddleware
from typing_extensions import TypedDict

from chatbot_model import get_model
from personas import PERSONAS


def get_persona_chain(question):
    model = get_model()
    persona_chain = (PromptTemplate.from_template(
        """Given the user question below, detect the country that the content of the question has the biggest relation to as its english name.
                        Differentiate between the countries 'sweden', 'denmark', 'lithuania', 'iceland', 'norway', 'latvia',
                        'finland', 'poland', 'germany', 'estonia'.

                        Do not respond with more than one word or uppercase letters.

                        <question>
                        {question}
                        </question>

                        Classification:"""
    )
                     | model
                     | StrOutputParser()
                     )
    answer = persona_chain.invoke({'question': question})
    return answer


def create_persona_chain(country, question):
    if country == "group":
        generated_country = get_persona_chain(question)[:3].lower()
        prompt_character = ChatPromptTemplate.from_messages([
            ('system', f"You are the following person: {PERSONAS[generated_country]}")
        ])
    else:
        prompt_character = ChatPromptTemplate.from_messages([
            ('system', f"You are the following person: {PERSONAS[country]}")
        ])
    return prompt_character


branch = RunnableLambda(
    lambda x: create_persona_chain(x['topic'], x['question'])
)
