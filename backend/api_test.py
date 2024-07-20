import os
import uuid
from typing import Any, Dict

from fastapi import HTTPException, Request
from langchain_openai import ChatOpenAI

from history_chain import chain_with_history
from language_chain import language_chain
from tone_chain import tone_chain
from topic_chain import branch
from topic_chain import get_persona_chain

# Initialize OpenAI client
LLM_ENDPOINT = os.environ.get("LLM_ENDPOINT", "https://chat-large.llm.mylab.th-luebeck.dev/v1")
API_KEY = os.environ.get("API_KEY", "-")
model = ChatOpenAI(streaming=True, api_key=API_KEY, model="gpt-4o-mini")


def _per_request_config_modifier(
    config: Dict[str, Any], request: Request
) -> Dict[str, Any]:
    """Update the config"""
    config = config.copy()
    configurable = config.get("configurable", {})
    # Look for a cookie named "user_id"
    user_id = request.cookies.get("user_id", None)

    if user_id is None:
        raise HTTPException(
            status_code=400,
            detail="No user id found. Please set a cookie named 'user_id'.",
        )

    configurable["user_id"] = user_id
    config["configurable"] = configurable
    return config


full_chain = {"topic": lambda x: x["topic"], "question": lambda x: x["question"], "input": lambda x: x["question"],
              'answer_tone': tone_chain, 'character': branch,  'new_topic': lambda x: get_persona_chain(x['topic'], x['question'])[:3].lower(), 'language': language_chain} | chain_with_history

if __name__ == "__main__":
    conversation_id = str(uuid.uuid4())
    configuration = {'configurable': {'conversation_id': conversation_id, 'user_id': 'textuser'}}
    out = full_chain.invoke({"topic": "swe", "question": "Tell me about yourself"}, configuration)
    print(out)

    # out2 = full_chain.invoke({"topic": "swe", "question": "Tell me something about studying in sweden."}, configuration)
    # print(out2)

    # out3 = full_chain.invoke({"topic": "swe", "question": "What did I ask you before?"}, configuration)
    # print(out3)
