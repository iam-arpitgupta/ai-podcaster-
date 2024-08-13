import os
from groq import Groq

def query_groq(prompt, history):
    try:
        # Configure the Groq client
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        # Prepare the messages for the API
        messages = [
            {"role": "system", "content": "You are a hardcore Tech nerd Anti-Ai"}
        ]
        recent_history = history[-4:] if len(history) > 4 else history
        for i, msg in enumerate(recent_history):
            role = "user" if i % 2 == 0 else "assistant"
            messages.append({"role": role, "content": msg})
        messages.append({"role": "user", "content": prompt})
        
        # Make the API request
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="mixtral-8x7b-32768",  # You can change this to other available models
            max_tokens=200
        )
        
        # Extract the response content
        return chat_completion.choices[0].message.content
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None