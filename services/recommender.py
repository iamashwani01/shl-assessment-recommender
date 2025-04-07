import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()  

HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

async def get_recommendation(job_role: str, competencies: str) -> str:
    prompt = (
        f"You are an expert in HR assessment design. "
        f"Suggest the best SHL assessments for the following:\n\n"
        f"Job Role: {job_role}\n"
        f"Competencies: {competencies}\n\n"
        f"List only the most suitable assessments with a short explanation for each."
    )

    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 500,
            "return_full_text": False
        }
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(HUGGINGFACE_API_URL, headers=headers, json=payload)

        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"].strip()
        else:
            return f"❌ Error from Hugging Face API: {result}"

    except Exception as e:
        return f"🔥 Exception occurred: {str(e)}"
