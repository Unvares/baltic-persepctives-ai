from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prompts import get_chain
from langserve import add_routes

chain = get_chain()

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
    chain,
    path="/openai",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
