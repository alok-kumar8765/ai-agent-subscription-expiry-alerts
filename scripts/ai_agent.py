import os
import openai
import requests
import subprocess

def ai_generate_message(text):
    try:
        key = open("config/openai_key.txt").read().strip()
        openai.api_key = key
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": text}]
        )
        return completion['choices'][0]['message']['content']
    except:
        print("⚠ Switching to local AI model (Llama).")
        result = subprocess.run(
            ["python", "local_ai/run_local_llama.py", text],
            capture_output=True, text=True
        )
        return result.stdout
