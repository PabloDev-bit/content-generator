import types
import unittest
from unittest.mock import patch

from app import app

class GenerateEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.testing = True

    @patch('app.openai.ChatCompletion.create')
    def test_generate_endpoint(self, mock_create):
        # Prepare mocked response similar to OpenAI's structure
        mock_create.return_value = types.SimpleNamespace(
            choices=[types.SimpleNamespace(
                message=types.SimpleNamespace(content="Voici une réponse générée")
            )]
        )

        response = self.client.post('/generate', json={'prompt': 'Question fictive'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('result', data)
        self.assertEqual(data['result'], 'Voici une réponse générée')

    @patch('app.openai.Image.create')
    def test_generate_image_endpoint(self, mock_image_create):
        mock_image_create.return_value = {
            'data': [{'url': 'http://example.com/image.png'}]
        }
        response = self.client.post('/generate-image', json={'prompt': 'un chat'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('image_url', data)
        self.assertEqual(data['image_url'], 'http://example.com/image.png')

if __name__ == '__main__':
    unittest.main()
