
# Import our AI function from another file
from ollama_client import ask_ollama

# Send a test message to the local AI
result = ask_ollama(
    "Reply exactly with: Local AI connection successful!"
)

# Display the AI response
print(result)
