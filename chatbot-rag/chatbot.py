import os
import streamlit as st
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "-")
LLM_ENDPOINT = os.environ.get("LLM_ENDPOINT", "https://chat-large.llm.mylab.th-luebeck.dev/v1")
EMBEDDING_EP = os.environ.get("EMBEDDING_EP", "https://bge-m3-embedding.llm.mylab.th-luebeck.dev/")

embeddings = HuggingFaceEndpointEmbeddings(model=EMBEDDING_EP)
llm = OpenAI(base_url=LLM_ENDPOINT, api_key=OPENAI_API_KEY)
vectorstore = Chroma(embedding_function=embeddings, persist_directory="/data")

st.set_page_config(page_title="KIRA", page_icon="🦜", menu_items={})
st.title("🦜 Ask me anything ...")
st.markdown("## ... about prompt engineering")

system_prompt = [{
    "role": "system", 
    "content": " ".join([
        "Your name is KIRA and you are a prompt engineering expert.",
        "You answer questions only based on your context queried from your reliable knowledge store.",
        "If you provide links, references or sources, you do this only on facts found in your context."
    ])
}]

st.session_state['messages'] = st.session_state.get('messages', [])

# Show previous messages
for entry in st.session_state['messages']:
    with st.chat_message(entry['role']):
        st.write(entry['content'])

# Handle the user prompt and stream a response
if prompt := st.chat_input("🦜 Ask me anything about prompt engineering ..."):
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("ai"):
        with st.status("Querying knowledge base"):
            retriever = vectorstore.as_retriever(search_kwargs={'k': 3})
            last_response = st.session_state.messages[-1]['content'] if st.session_state.messages else ""
            ctx = '\n\n'.join(c.page_content for c in retriever.invoke(last_response + "\n" + prompt))
            st.write(f"Found a context with {len(ctx)} characters.")

        last_messages = st.session_state.messages[-2:] if len(st.session_state.messages) > 2 else st.session_state.messages
        completion = llm.chat.completions.create(
            messages=system_prompt + [{ "role": "system", "content": f"Context: {ctx[0:17500]}" }] + last_messages + [
                { "role": "user", "content": prompt }
            ],
            model="", stream=True, max_tokens=1000
        )
        response = st.write_stream(m.choices[0].delta.content for m in completion if not m.choices[0].finish_reason)
        st.session_state.messages.extend([
            { "role": "user", "content": prompt },
            { "role": "ai", "content": response },
        ])