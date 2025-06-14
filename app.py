import os
from flask import Flask, request, jsonify
import openai

# Configure OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json(silent=True)
    if not data or 'prompt' not in data:
        return jsonify({'error': 'Missing prompt'}), 400
    prompt = data['prompt']
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        result_text = response.choices[0].message.content.strip()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'result': result_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
