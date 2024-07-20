from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnableLambda

from chatbot_model import get_model
from personas import PERSONAS


def get_persona_chain(topic, question):
    if topic == "group":
        model = get_model()
        persona_chain = (PromptTemplate.from_template(
            """Given the user question below, detect the country that the content of the question has the biggest relation to as its english name.
                            Differentiate between the countries 'sweden', 'denmark', 'lithuania', 'iceland', 'norway', 'latvia',
                            'finland', 'poland', 'germany', 'estonia'. If you cant find no matches use 'poland' as the value.

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
    return topic


def create_persona_chain(country, question):
    if country == "group":
        generated_country = get_persona_chain(country, question)[:3].lower()
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
