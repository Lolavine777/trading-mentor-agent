import os
import sys
import io
import google.generativeai as genai
from dotenv import load_dotenv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

print("Models:")
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)
