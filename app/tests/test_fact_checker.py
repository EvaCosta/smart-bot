import pytest
from unittest.mock import MagicMock, patch
from app.fact_checker import FactChecker
import numpy as np

def test_fact_checker_initialization():
    checker = FactChecker()
    assert checker.model is not None
    assert len(checker.known_facts_embeddings) == len(checker.known_facts)

def test_validate_input_known_fact():
    checker = FactChecker()

    # Mock do método _compute_similarity para retornar alta similaridade
    checker._compute_similarity = MagicMock(return_value=np.array([[0.95]]))

    user_input = "A Terra é redonda."
    assert checker.validate_input(user_input) is True

def test_validate_input_unknown_fact_with_google_success():
    checker = FactChecker()

    # Mock do método _compute_similarity para retornar baixa similaridade
    checker._compute_similarity = MagicMock(return_value=np.array([[0.5]]))

    # Mock para simular uma resposta bem-sucedida do Google Knowledge Graph
    with patch("app.fact_checker.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "itemListElement": [{"result": {"name": "Fato verificado"}}]
        }
        mock_get.return_value = mock_response

        user_input = "O sol é quente."
        result = checker.validate_input(user_input)
        assert result == {"name": "Fato verificado"}

def test_validate_input_unknown_fact_with_google_failure():
    checker = FactChecker()

    # Mock do método _compute_similarity para retornar baixa similaridade
    checker._compute_similarity = MagicMock(return_value=np.array([[0.5]]))

    # Mock para simular uma falha na API do Google Knowledge Graph
    with patch("app.fact_checker.requests.get", side_effect=Exception("Erro na API")):
        user_input = "O sol é quente."
        result = checker.validate_input(user_input)
        assert result == {}

def test_compute_similarity():
    checker = FactChecker()
    
    # Mock dos embeddings com dimensões reais (384 neste caso)
    embeddings = np.random.rand(2, 384)
    query_embedding = np.random.rand(1, 384)
    
    # Mock do método _generate_embeddings
    checker._generate_embeddings = MagicMock(return_value=embeddings)
    checker.known_facts_embeddings = embeddings
    
    # Verificar se a similaridade está correta
    similarity = checker._compute_similarity(query_embedding)
    assert similarity is not None


def test_google_api_integration():
    checker = FactChecker()

    # Mock para simular uma resposta bem-sucedida da API
    with patch("app.fact_checker.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "itemListElement": [{"result": {"name": "Fato verificado"}}]
        }
        mock_get.return_value = mock_response

        user_input = "A Lua é um satélite natural."
        result = checker._verify_with_google_knowledge_graph(user_input)
        assert result == {"name": "Fato verificado"}
