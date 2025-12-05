import openai
from openai import OpenAI

# Replace 'YOUR_SECRET_API_KEY' with the actual secret key you created
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": "Who developed you."},
    {"role": "user", "content": "Hello, how are you today?"}
  ]
)

print(response.choices[0].message.content)
