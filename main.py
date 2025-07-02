import ollama
import requests

OLLAMA_MODEL = 'exaone-deep:2.4b'  # Replace with your local model name

# Ask the user for a research question
user_question = input("Enter your research question or topic: ")

# Step 1: Ask the model for keywords to search
initial_prompt = [
    {
        'role': 'system',
        'content': (
            "You are an AI assistant for research. "
            f"Suggest 3 keywords or phrases relevant to: {user_question} "
            "ONLY respond with a Python list of strings."
        )
    }
]

keyword_response = ollama.chat(
    model=OLLAMA_MODEL,
    messages=initial_prompt
)


# Extract keywords from the model's response (with debug and safer parsing)
import ast
print("Model response:", keyword_response['message']['content'])
try:
    keywords = ast.literal_eval(keyword_response['message']['content'])
    if not isinstance(keywords, list):
        raise ValueError
except Exception:
    print("Failed to parse keywords from model response.")
    keywords = ['bbc news']
print("Keywords:", keywords)

# Step 2: Fetch news for each keyword
news_data = []
for query in keywords:
    url = (
        'https://newsapi.org/v2/everything?'
        f'q={query}&'
        'sortBy=popularity&'
        'apiKey=bb133df896384f8282292ca1b1c12c07'
    )
    response = requests.get(url)
    news_data.append(response.json())

# Step 3: Feed the news data back to the model for analysis
messages = [
    {
        'role': 'system',
        'content': (
            "You are an AI that analyzes stock and economic news. "
            "You will be given recent news articles for selected keywords. "
            "After reading the data, respond ONLY with your prediction for the next month in the format '£xxxx.xx'."
        )
    }
]

for i, data in enumerate(news_data):
    messages.append({
        'role': 'user',
        'content': f"News data for keyword '{keywords[i]}': {data}"
    })

response = ollama.chat(
    model=OLLAMA_MODEL,
    messages=messages
)

