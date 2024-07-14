import requests

url = 'http://localhost:5000/ask_claude'
data = {
    'user_input': 'Can you tell me about your experience with UX research?'
}
headers = {'Content-Type': 'application/json'}
response = requests.post(url, json=data, headers=headers)
print(response.json())