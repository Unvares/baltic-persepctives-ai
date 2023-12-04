import streamlit as st
from text_generation import Client
from langchain.prompts import PromptTemplate
import os

llama2 = Client(os.environ.get("LLM_TGI_URL", "https://em-german-70b.llm.mylab.th-luebeck.dev"))

vicuna       = PromptTemplate.from_template("{context}\n\nUSER:\n{prompt}\n\nASSISTANT:\n")
vicuna_chat  = PromptTemplate.from_template("{role}\n{text}\n")
vicuna_roles = { 'system': '', 'user': 'USER:', 'ai': 'ASSISTANT:' }

from tokenizers import Tokenizer
tokenizer = Tokenizer.from_pretrained("bert-base-cased")

st.set_page_config(
    page_title="KIRA",
    page_icon="🧠",
    layout="wide",
    menu_items={}
)

st.markdown("""
<style>
#MainMenu, .stDeployButton {
    visibility: hidden;
}
            
.hackathon {
    margin: 1em;
    padding: 1em;
    text-decoration: none !important;
    color: white !important;
    background: #E40039 !important;
    border-radius: 0.25em;
}
</style>
""", unsafe_allow_html=True)


system = " ".join([
    "Du heißt KIRA und bist eine detailliert Auskunft gebende Assistentin.",
    "KIRA steht für 'künstlich intelligente Recherche Anwendung'.",
    "KIRA steht aber auch für die Mitarbeiterin Kira Rösinger.",
    "Kira Rösinger ist die 'gute Seele' des Bereichs Forschung und Transfer der THL."
    "Du bist der ChatBot der Technischen Hochschule Lübeck (TH-Lübeck oder THL).",
    "Prof. Nane Kratzke hat dich mit Studenten gemeinsam entwickelt.",
    "Du arbeitest mit dem Sprachmodell (LLM) EM German 13B (ein für deutsch getunetes Llama2 LLM).",
    "Du wurdest als Demo-Anwendung für den Hanseatic Hackathon (2023) entwickelt."
])


st.session_state['discussion'] = st.session_state.get('discussion', [{
    'role': 'system',
    'text': system,
    'tokens': len(tokenizer.encode(system))
}])

with st.sidebar:
    st.markdown(f"""
        <center>
            <a href='https://mylab.th-luebeck.de'>
                <img src='https://mylab.th-luebeck.de/images/mylab-logo-without.png' height='60px' />
            </a>
            <br>
            <img src='https://cdn-icons-png.flaticon.com/512/2911/2911380.png' height=100px' />
        </center>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <center>
            <h1>myLab Llama aka KIRA</h1>
            Funktioniert auch auf deinem Smartphone:
            <br>
            <img src='https://qr.mylab.th-luebeck.dev?data=https://kira.mylab.th-luebeck.dev'>
            <br>
            <br>
            Powered by
            <br>
            <strong><a href="https://huggingface.co/TheBloke/em_german_70b_v01-AWQ">EM German 70B (Llama2)</a></strong>
            <br>
            (on-premise, no cloud, no data sniffing)
            <br>
            Wir respektieren deine Privatsphäre.
        <center>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <center>
            <hr>
            Eine Demo-Applikation für den
            <br>
            <br>
            <a href="https://hanse-innovation-campus.de/de/hanseatic-hackathon" class="hackathon">Hanseatic Hackathon 2023</a>
            <br>
            <br>
            <hr>
            <a href="https://www.th-luebeck.de/hiluebeck/">
                <img src='https://www.th-luebeck.de/fileadmin/media/Landingpages_TYPO3/hi-luebeck/img/logo_innovative_hochschule.png' width=50%>
            </a>
            <br>
            <br>
            <small>
                <a href='https://mylab.th-luebeck.de/impressum'>Impressum</a> &bullet;
                <a href='https://mylab.th-luebeck.de/datenschutz'>Datenschutz</a><br>
                <a href='https://mylab.th-luebeck.de/nutzungsbedingungen'>Nutzungsbedingungen</a> &bullet;
                <a href='https://mylab.th-luebeck.de/haftungsausschluesse'>Haftungsausschlüsse</a><br>
            </small>
        </center>
    """, unsafe_allow_html=True)

prompt = st.chat_input("I am a stochastic parrot / Ich bin ein stochastischer Papagei. Frag mich etwas / Ask me anything ...")

def add_prompt(prompt):
    # Build up the context
    context = ""
    memory = 0
    for n, entry in enumerate(st.session_state['discussion'][::-1]):
        memory += entry['tokens']
        if memory > 3000:
            break

    # Show the conversation history
    for entry in st.session_state['discussion']:
        if entry['role'] in ['user', 'ai']:
            with st.chat_message(entry['role']):
                st.markdown(entry['text'])

    with st.chat_message('user'):
        st.write(prompt.strip())

    with st.chat_message('ai'):
        placeholder = st.markdown("")
        text = ""

        conversation = [(vicuna_roles[e['role']], e['text']) for e in st.session_state['discussion'][n:]]
        for response in llama2.generate_stream(
            vicuna.format(
                context = "\n\n".join(vicuna_chat.format(role=r, text=t).strip() for r, t in conversation),
                prompt  = prompt
            ), 
            temperature=0.25, 
            repetition_penalty=1.1,
            max_new_tokens=1024
        ):
            if response.token.special:
                continue

            text += response.token.text
            placeholder.markdown(text)

    st.link_button("Neues Gespräch", "https://kira.mylab.th-luebeck.dev", type="secondary")

    st.session_state['discussion'].extend([{
        'role': 'user',
        'text': prompt,
        'tokens': len(tokenizer.encode(prompt))
    }, {
        'role': 'ai',
        'text': response.generated_text,
        'tokens': response.details.generated_tokens
    }])


if prompt:
    add_prompt(prompt)