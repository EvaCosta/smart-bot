import pytest
from unittest.mock import MagicMock

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


from ..chatbot import Chatbot
from ..langchain_api import LangChainAPI
from ..vector_database import VectorDatabase


# Teste para quando o input do usuário for inválido
def test_invalid_input():
    chatbot = Chatbot()

    # Testando se a resposta é a esperada para uma entrada inválida
    response = chatbot.respond("ab")
    assert response == "Entrada inválida, por favor tente novamente."

# Teste para quando o input do usuário for válido e a resposta já existir no banco
def test_existing_response():
    chatbot = Chatbot()

    # Mock do método query do VectorDatabase para retornar uma resposta existente
    chatbot.db.query = MagicMock(return_value="Resposta existente")

    # Testando se a resposta já existente é retornada
    response = chatbot.respond("Qual é a capital da França?")
    assert response == "Resposta existente"
    chatbot.db.query.assert_called_once_with("Qual é a capital da França?")

# Teste para quando o input do usuário for válido e não houver resposta existente
def test_generate_and_save_response():
    chatbot = Chatbot()

    # Mock do método query do VectorDatabase para retornar None (não existe resposta)
    chatbot.db.query = MagicMock(return_value=None)

    # Mock do método generate_response do LangChainAPI para gerar uma resposta simulada
    chatbot.api.generate_response = MagicMock(return_value="Paris")

    # Mock do método save do VectorDatabase para garantir que a resposta gerada seja salva
    chatbot.db.save = MagicMock()

    # Testando a geração de resposta
    response = chatbot.respond("Qual é a capital da França?")
    assert response == "Paris"
    chatbot.api.generate_response.assert_called_once_with("Qual é a capital da França?", None, "informal")
    chatbot.db.save.assert_called_once_with("Qual é a capital da França?", "Paris")

# Teste para a função _is_valid_input
def test_is_valid_input():
    chatbot = Chatbot()

    # Testando entradas válidas e inválidas
    assert chatbot._is_valid_input("Isso é válido")
    assert not chatbot._is_valid_input("ab")

# Teste para o erro de API (mockando a falha no LangChainAPI)
def test_api_error():
    chatbot = Chatbot()

    # Simulando um erro ao chamar o método generate_response
    chatbot.api.generate_response = MagicMock(side_effect=Exception("Erro de API"))

    response = chatbot.respond("Qual é a capital da França?")
    assert "Erro ao gerar resposta" in response
