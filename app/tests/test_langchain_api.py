import pytest
from unittest.mock import MagicMock, patch
from langchain_api import LangChainAPI

class MockDelta:
    def __init__(self, content):
        self.content = content

class MockChoice:
    def __init__(self, delta):
        self.delta = delta

class MockChunk:
    def __init__(self, choices):
        self.choices = choices

def test_initialization_with_missing_api_key():
    with patch("os.getenv", return_value=None):
        with pytest.raises(ValueError, match="API_KEY não configurada. Verifique o arquivo .env."):
            LangChainAPI()

def test_generate_response_success():
    # Mock da variável de ambiente
    with patch("os.getenv", return_value="fake_api_key"):
        api = LangChainAPI()

        # Mock do cliente Groq
        api.client = MagicMock()
        api.client.chat.completions.create.return_value = iter([
            MockChunk(choices=[MockChoice(delta=MockDelta(content="Resposta gerada"))]),
            MockChunk(choices=[MockChoice(delta=MockDelta(content=None))]),
        ])

        # Teste de geração de resposta
        prompt = "Qual é a capital da França?"
        response = api.generate_response(prompt)
        assert response == "Resposta gerada"

        api.client.chat.completions.create.assert_called_once_with(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
        )

def test_generate_response_error():
    # Mock da variável de ambiente
    with patch("os.getenv", return_value="fake_api_key"):
        api = LangChainAPI()

        # Mock do cliente Groq com exceção
        api.client = MagicMock()
        api.client.chat.completions.create.side_effect = Exception("Erro simulado")

        # Teste de tratamento de erro
        prompt = "Qual é a capital da França?"
        response = api.generate_response(prompt)
        assert "Erro ao gerar resposta" in response
        assert "Erro simulado" in response

        api.client.chat.completions.create.assert_called_once_with(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
        )
