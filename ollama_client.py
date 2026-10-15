import requests

# Ollama local API address
OLLAMA_URL = "http://localhost:11434/api/chat"

# Local AI model name
MODEL_NAME = "qwen2.5:0.5b"


def ask_ollama(prompt):
    """
    Send a prompt to Ollama and return the AI response.
    """

    # Check whether the user entered anything
    if not prompt or not prompt.strip():
        return "Please enter some text."

    try:
        # Send the prompt to the local AI model
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False
            },
            timeout=240
        )

        # Raise an error if the request failed
        response.raise_for_status()

        # Convert the response into Python dictionary
        data = response.json()

        # Extract and return the AI's reply
        answer = data.get("message", {}).get("content", "")

        if not answer.strip():
            return "The AI returned an empty response. Please try again."

        return answer.strip()

    except requests.exceptions.ConnectionError:
        return (
            "Cannot connect to Ollama. "
            "Please make sure Ollama is running."
        )

    except requests.exceptions.Timeout:
        return (
            "The AI took too long to respond. "
            "Please try again with shorter input."
        )

    except requests.exceptions.RequestException as error:
        return f"Connection error: {error}"

    except (ValueError, AttributeError) as error:
        return f"Could not process the AI response: {error}"
