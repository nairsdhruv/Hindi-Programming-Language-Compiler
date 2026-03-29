from google import genai
from dotenv import load_dotenv
import os
import certifi

# SSL FIX
os.environ["SSL_CERT_FILE"] = certifi.where()

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_gemini(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
        config={
            "temperature": 0.0,
            "max_output_tokens": 300,
        }
    )

    if response.text:
        return response.text.strip()

    try:
        return response.candidates[0].content.parts[0].text.strip()
    except:
        return "❌ No output"


if __name__ == "__main__":
    output = generate_gemini("Say hello clearly")
    print("OUTPUT:", output)

