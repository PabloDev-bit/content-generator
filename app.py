import os
from flask import Flask, request, jsonify, render_template
import openai

# Configure OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    """Render the homepage with the simple form."""
    return render_template('index.html')

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


@app.route('/generate-image', methods=['POST'])
def generate_image():
    """Generate an image using DALL·E and return its URL."""
    data = request.get_json(silent=True)
    if not data or 'prompt' not in data or not isinstance(data['prompt'], str):
        return jsonify({'error': 'Missing or invalid prompt'}), 400
    prompt = data['prompt'].strip()
    print(f"Received prompt: {prompt}")

    if not openai.api_key:
        return jsonify({'error': 'OpenAI API key is not configured'}), 500

    try:
        response = openai.Image.create(prompt=prompt, n=1, size="512x512")
        print(f"DALL·E response: {response}")
        if not response or 'data' not in response or not response['data']:
            return jsonify({'error': 'Empty response from OpenAI'}), 500
        image_url = response['data'][0].get('url')
        if not image_url:
            return jsonify({'error': 'No image URL returned'}), 500
    except Exception as e:
        print(f"Error generating image: {e}")
        return jsonify({'error': str(e)}), 500
    return jsonify({'image_url': image_url})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
