import os
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "In one sentence, what is a coding agent?"}
    ],
)

print(response.choices[0].message.content)
