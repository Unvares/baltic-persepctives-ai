# Achtung: Dies ist nur ein sehr einfaches und nicht sonderlich effizientes Beispiel für die Indizierung
# einer Datenquelle (hier: Liste von deutschen Witzen).
# Es ist bspw. ratsam nur neue Dokumente zu indizieren und nicht jedesmal den Index komplett neu aufzubauen.
#
import requests
import chromadb
import os
import shutil
from langchain.vectorstores import Chroma
from langchain.embeddings import LocalAIEmbeddings
from langchain.schema.document import Document

EMBEDDINGS_ENDPOINT = os.environ.get("EMBEDDINGS_ENDPOINT", "https://embeddings.llm.mylab.th-luebeck.dev")
DB_PATH = os.environ.get("DB_PATH", "/data/chromadb")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "witze")

try:
    print("Lösche bereits erstellten Index.")
    shutil.rmtree(DB_PATH)
except Exception as ex:
    print(f"Kein Index gefunden. {ex}")

persistent_client = chromadb.PersistentClient(path=DB_PATH)
collection = persistent_client.get_or_create_collection(COLLECTION_NAME)

vs = Chroma(
    client=persistent_client,
    collection_name="witze",
    embedding_function=LocalAIEmbeddings(
        openai_api_base=EMBEDDINGS_ENDPOINT, 
        openai_api_key="for-free",           # Den Key kann man sich ausdenken, er darf nur nicht leer sein.
        model="default-sd"                   # Oder default-hd für langsamere aber bessere Embeddings
    ),
    collection_metadata={"hnsw:space": "cosine"} # Nutze 'ip' für default-hd
)

print("Es befinden sich", vs._collection.count(), "Dokumente im Index.")

resp = requests.get("https://raw.githubusercontent.com/spacerace/dos-fortune/master/dist/intl/de/witze")
witze = resp.content.decode().split("\n%\n")

print("Indizierung von", len(witze), "Dokumenten läuft.")

docs = [Document(page_content=witz.strip(), metadata={"source": "local"}) for witz in witze if witz.strip()]
ids = vs.add_documents(docs)

print(len(ids), "Dokumente wurden dem Index erfolgreich hinzugefügt.")
