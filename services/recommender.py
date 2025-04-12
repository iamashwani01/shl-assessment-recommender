import httpx
import asyncio
import os
import json
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

async def get_recommendation(query: str) -> list:
    prompt = (
        f"You are an expert in SHL assessments. Based on the following job description or query:\n\n"
        f"{query}\n\n"
        f"Return a JSON list of 1-3 recommended SHL assessments in this format:\n"
        f"[\n"
        f"  {{\n"
        f"    \"url\": \"https://...\",\n"
        f"    \"adaptive_support\": \"Yes/No\",\n"
        f"    \"description\": \"short explanation\",\n"
        f"    \"duration\": 60,\n"
        f"    \"remote_support\": \"Yes/No\",\n"
        f"    \"test_type\": [\"Cognitive\", \"Behavioral\"]\n"
        f"  }}\n"
        f"]"
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
        
        # Check if the response is valid
        if response.status_code != 200:
            return [{
                "url": "",
                "adaptive_support": "No",
                "description": f"❌ API error: {response.status_code} - {response.text}",
                "duration": 0,
                "remote_support": "No",
                "test_type": []
            }]
        
        result = response.json()

        # Check if the result is valid
        if isinstance(result, list) and "generated_text" in result[0]:
            text = result[0]["generated_text"].strip()
            return json.loads(text)
        else:
            return [{
                "url": "",
                "adaptive_support": "No",
                "description": f"❌ Error: Invalid response format from Hugging Face API",
                "duration": 0,
                "remote_support": "No",
                "test_type": []
            }]
    
    except httpx.RequestError as e:
        # Handle network or request-related errors
        return [{
            "url": "",
            "adaptive_support": "No",
            "description": f"🔥 RequestError: {str(e)}",
            "duration": 0,
            "remote_support": "No",
            "test_type": []
        }]
    
    except httpx.TimeoutException:
        # Handle timeout errors
        return [{
            "url": "",
            "adaptive_support": "No",
            "description": "🔥 Request Timeout: The request took too long to respond.",
            "duration": 0,
            "remote_support": "No",
            "test_type": []
        }]
    
    except Exception as e:
        # Handle any other exceptions
        return [{
            "url": "",
            "adaptive_support": "No",
            "description": f"🔥 Exception occurred: {str(e)}",
            "duration": 0,
            "remote_support": "No",
            "test_type": []
        }]
