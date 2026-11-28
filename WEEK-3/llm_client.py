import requests
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"


def generate_response(prompt):
    start_time = time.time()

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()
        result = response.json()

        end_time = time.time()

        input_tokens = result.get("prompt_eval_count", 0)
        output_tokens = result.get("eval_count", 0)

        return {
            "success": True,
            "response": result.get("response", ""),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "response_time": round(end_time - start_time, 3)
        }

    except requests.exceptions.RequestException as error:
        return {
            "success": False,
            "response": str(error),
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "response_time": round(time.time() - start_time, 3)
        }