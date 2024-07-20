from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from chatbot_model import get_model

model = get_model()

language_chain = (PromptTemplate.from_template(
    """Given the user question below, detect its language and return the result.

    Do not respond with more than one word.

    <question>
    {question}
    </question>

    Classification:"""
)
                  | model
                  | StrOutputParser()
                  )
