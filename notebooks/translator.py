from openai import OpenAI

client = OpenAI(
    base_url="https://chat-large.llm.mylab.th-luebeck.dev/v1",
    api_key="-"
)

chat_completion = client.chat.completions.create(
    # Prompt (sequence of system-, user-, and ai-messages)
    messages=[{ 
        "role": "system", 
        "content": "You translate texts into English." 
    }, {
        "role": "user", 
        "content": "Lübeck ist die Königin der Hanse."
    }],
    model="", stream=True, max_tokens=1024 # Parameters
)

for message in chat_completion:
    if not message.choices[0].finish_reason:
        print(message.choices[0].delta.content, end='')