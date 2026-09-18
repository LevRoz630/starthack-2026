"""One chat interface over OpenAI-compatible endpoints.

Apertus on Swisscom comes first so client data stays in Switzerland; OpenAI is the
fallback. A provider is skipped when its key is missing from .env.
"""

import os

import requests
from dotenv import load_dotenv

from .data import ROOT

load_dotenv(ROOT / '.env')

PROVIDERS = [
    {'name': 'apertus', 'key_env': 'SWISSCOM_KEY', 'model': 'swiss-ai/Apertus-v1.5-70B',
     'url': 'https://api.swisscom.com/products/swiss-ai-weeks/apertus-1.5-70b/v1/chat/completions'},
    {'name': 'openai', 'key_env': 'OPENAI_API_KEY', 'model': os.getenv('OPENAI_MODEL', 'gpt-4.1-mini'),
     'url': 'https://api.openai.com/v1/chat/completions'},
]


class LLMUnavailable(RuntimeError):
    pass


def chat(messages, temperature=0.2, max_tokens=600, timeout=20):
    """Return (text, provider name) from the first provider that answers."""
    errors = []
    for provider in PROVIDERS:
        key = (os.getenv(provider['key_env']) or '').strip().strip('"\'')
        if not key:
            continue
        try:
            resp = requests.post(
                provider['url'],
                headers={'Authorization': f'Bearer {key}'},
                json={'model': provider['model'], 'messages': messages,
                      'temperature': temperature, 'max_tokens': max_tokens},
                timeout=timeout)
            resp.raise_for_status()
            return resp.json()['choices'][0]['message']['content'], provider['name']
        except (requests.RequestException, KeyError, IndexError, ValueError) as e:
            errors.append(f'{provider["name"]}: {e}')
    raise LLMUnavailable('; '.join(errors) or 'no LLM key configured')
