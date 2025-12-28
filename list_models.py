import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

models = genai.list_models()

print("\nAVAILABLE MODELS:\n")
for m in models:
    print("MODEL:", m.name)
    print("SUPPORTED METHODS:", m.supported_generation_methods)
    print("-" * 60)
