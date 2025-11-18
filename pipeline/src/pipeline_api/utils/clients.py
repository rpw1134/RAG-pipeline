from openai import OpenAI
import os

openai_client: OpenAI = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
