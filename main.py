
import openai
import json
import os

# Load API key from config file
config_file = "config.json"
if os.path.exists(config_file):
    with open(config_file, "r") as f:
        config = json.load(f)
    openai.api_key = config["openai_api_key"]
else:
    raise FileNotFoundError("Config file not found! Please create a 'config.json' file with the API key.")

# Path to the JSON file where conversation history will be stored
history_file = "conversation_history.json"

# Load conversation from the JSON file if it exists, otherwise start fresh
if os.path.exists(history_file):
    with open(history_file, "r") as f:
        conversation = json.load(f)
else:
    # Initialize with a system message if no prior history exists
    conversation = [
        {"role": "system", "content": "Welcome to the assistant! Feel free to ask anything."}
    ]

def ask_gpt(prompt):
    # Add the user's input to the conversation history
    conversation.append({"role": "user", "content": prompt})
    
    # Make the API call with the entire conversation history
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=conversation
    )
    
    # Extract the assistant's message
    assistant_message = response.choices[0].message.content
    
    # Add the assistant's response to the conversation history
    conversation.append({"role": "assistant", "content": assistant_message})
    
    # Save the conversation to the JSON file after each interaction
    with open(history_file, "w") as f:
        json.dump(conversation, f, indent=4)
    
    return assistant_message

while True:
    user_prompt = input("> ")
    if user_prompt.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break
    print(ask_gpt(user_prompt))

