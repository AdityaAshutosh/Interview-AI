from flask import Flask, request, jsonify
import pandas as pd
import anthropic
import random
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load the dataset
csv_path= "C:/Users/ASUS/OneDrive/Documents/Python Scripts/Interview AI/data/ux_user_interview_questions.csv"
questions_df = pd.read_csv(csv_path)


API_KEY = os.getenv("API_KEY")
#API_VERSION = "2023-06-01"
claude = anthropic.Anthropic(api_key=API_KEY)
questions_list = questions_df.to_dict(orient='records')

@app.route('/')
def ask_claude():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    request_data = request.get_json()
    user_input = request_data.get('user_input')
    if not user_input:
        return jsonify({'error': 'User input is required'}), 400



  #Random question as convo starter
    question = random.choice(questions_list)['Question']

    print(f"User input: {user_input}")
    print(f"Selected question: {question}")

    try:
        response = claude.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": user_input},
                
            ]
        )
        print(f"API response: {response}")
        return jsonify(response)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Failed to get response from Claude API', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)