from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from chatbot_model import get_model

prompt_tone = ChatPromptTemplate.from_template("""
Is the following user prompt more passive or active?
By active I mean is user actively trying to forward a conversation.
By passive i mean asking generic questions or making generic statements.
Answer exactly "{active}" if tone is active or "{passive}" if tone is passive

Question: {question}
""")

passive_tone = """
Try to encourage user to ask more questions.
Try to forward the conversation.
"""

active_tone = """
Let the user lead conversation. Let them ask questions without your prompting
"""

model = get_model()
tone_chain = ({'passive': lambda x: passive_tone,
               'active': lambda x: active_tone,
               'question': lambda x: x['question']
               }
              | prompt_tone
              | model
              | StrOutputParser()
              )
