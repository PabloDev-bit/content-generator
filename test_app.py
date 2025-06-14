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

if __name__ == '__main__':
    unittest.main()
