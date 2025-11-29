import sys
from ollama import Client

client = Client()

prompt = sys.argv[1]

resp = client.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
print(resp['message']['content'])
