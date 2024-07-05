import os
import streamlit as st
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "-")
LLM_ENDPOINT = os.environ.get("LLM_ENDPOINT", "https://chat-large.llm.mylab.th-luebeck.dev/v1")
LLM_PREPROCESS_ENDPOINT = os.environ.get("LLM_ENDPOINT", "https://chat-slim.llm.mylab.th-luebeck.dev/v1")

EMBEDDING_ENDPOINT = os.environ.get("EMBEDDING_ENDPOINT", "")

if EMBEDDING_ENDPOINT:
    embeddings = OpenAIEmbeddings(base_url=LLM_ENDPOINT, api_key="-")
else:
    embeddings = OpenAIEmbeddings(api_key="sk-proj-M0N3AniQmJwCGttxwUn5T3BlbkFJ6VhsTuPbdauF8WeMrxRv")

llm = OpenAI(base_url=LLM_ENDPOINT, api_key=OPENAI_API_KEY)
preprocess_llm = OpenAI(base_url=LLM_PREPROCESS_ENDPOINT, api_key=OPENAI_API_KEY)

vectorstore = Chroma(embedding_function=embeddings, persist_directory="/data")


st.set_page_config(page_title="KIRA", page_icon="🦜", menu_items={})
st.title("🦜 Ask me anything ...")
st.markdown("## ... about prompt engineering")

st.session_state['messages'] = st.session_state.get('messages', [{
    "role": "system", 
    "content": "Your name is KIRA and you are a prompt engineering expert. If you have references, you link them in your responses."
}])

# Show previous messages
for entry in st.session_state['messages'][1:]:
    with st.chat_message(entry['role']):
        st.write(entry['content'])

# Handle the user prompt and stream a response
if prompt := st.chat_input("🦜 Ask me anything about prompt engineering ..."):
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("ai"):
        with st.status("Querying knowledge base"):
            retriever = vectorstore.as_retriever(search_kwargs={'k': 5})
            last_response = st.session_state.messages[-1]['content']
            ctx = '\n\n'.join(c.page_content for c in retriever.invoke(last_response + "\n" + prompt))
            st.write(f"Found a context with {len(ctx)} characters.")

        completion = llm.chat.completions.create(
            messages=st.session_state.messages + [
                { "role": "system", "content": f"Consider this context and references from your knowledge base in your answer. Context:\n\n{ctx}" },
                { "role": "user", "content": prompt }
            ],
            model="", stream=True, max_tokens=4000
        )
        response = st.write_stream(m.choices[0].delta.content for m in completion if not m.choices[0].finish_reason)
        st.session_state.messages.extend([
            { "role": "user", "content": prompt },
            { "role": "ai", "content": response },
        ])