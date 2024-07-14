from flask import Flask, request, jsonify
import pandas as pd
import random
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load the dataset
csv_path = "../data/ux_user_interview_questions.csv"
questions_df = pd.read_csv(csv_path)

# Claude 3 API configuration
API_KEY = os.getenv("API_KEY")
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

questions_list = questions_df.to_dict(orient='records')

@app.route('/')
def ask_claude():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify({'error': 'User input is required'}), 400

    # Select a random question from the dataset (you can implement more complex logic here)
    question = random.choice(questions_list)['Question']

    print(f"User input: {user_input}")
    print(f"Selected question: {question}")

    try:
        # Prepare the payload for the API request
        payload = {
            "model": "claude-3-opus-20240229",
            "max_tokens": 1024,
            "messages": [
                {"role": "user", "content": user_input},
            ]
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        # Send the request to the Claude API
        response = requests.post(CLAUDE_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        api_response = response.json()

        print(f"API response: {api_response}")
        return jsonify(api_response)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Failed to get response from Claude API', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
