import requests
import json

def CALLOLLAMA(user_message, model="phi3", history=[]):
    try:
        history_prompt = "\n".join(
            [f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}" for m in history]
        )
        final_prompt = f"{history_prompt}\nUser: {user_message}\nAssistant:"

        url = "http://localhost:11434/api/generate"
        payload = {
            "model": model,
            "prompt": final_prompt,
            "stream": False
        }

        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=120
        )

        if response.status_code == 200:
            result = response.json()
            return result.get("response", "Sorry, I didn't understand that.")
        else:
            return f"Error: {response.status_code}"

    except Exception as e:
        return f"Request failed: {str(e)}"
