from flask import Flask, jsonify, request
from openai import OpenAI
import os

app = Flask(__name__)

API_PASSWORD = os.environ.get('CHATGPT_SECRET_KEY', '')

@app.route('/gen', methods=['POST'])
def generate_film():
    password = request.headers.get('X-API-Password')
    if password != API_PASSWORD:
        return jsonify({'error': 'Unauthorized access'}), 401
    
    data = request.get_json()
    messages = data.get('messages', [])
    
    client = OpenAI()
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    response = completion.choices[0].message.content.strip()
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
