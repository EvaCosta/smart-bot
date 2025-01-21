import pytest
import numpy as np
import hashlib
from unittest.mock import MagicMock
from app.vector_database import VectorDatabase


@pytest.fixture
def vector_database():
    db = VectorDatabase()
    # Mockando o modelo de embeddings
    db.model.encode = MagicMock(return_value=np.random.rand(384).astype('float32'))
    # Mockando o fact_checker
    db.fact_checker.validate_input = MagicMock(return_value=True)
    return db


def test_save_valid_entry(vector_database):
    question = "Qual é a capital da França?"
    response = "Paris"

    vector_database.save(question, response)

    # Verifica se o vetor foi adicionado ao índice FAISS
    assert vector_database.index.ntotal == 1

    # Gera o hash do vetor para verificar se está no dicionário
    vector = vector_database.model.encode(question)
    vector_hash = hashlib.md5(vector.tobytes()).hexdigest()

    assert vector_database.data[vector_hash] == response


def test_query_existing_entry(vector_database):
    question = "Qual é a capital da França?"
    response = "Paris"

    # Salva a entrada para testar a consulta
    vector_database.save(question, response)

    # Consulta a mesma questão
    result = vector_database.query(question)

    assert result == response


def test_query_non_existing_entry(vector_database):
    question = "Qual é a capital da Alemanha?"

    # Consulta algo que não foi salvo
    result = vector_database.query(question)

    assert result is None


def test_save_fact_valid(vector_database):
    fact = "A água ferve a 100 graus Celsius ao nível do mar."
    
    # Salva o fato válido
    result = vector_database.save_fact(fact)
    
    assert result is True
    assert vector_database.index.ntotal == 1
    
    # Verifica se o fato foi armazenado corretamente
    vector = vector_database._embed(fact)  # Use _embed para garantir consistência
    vector_hash = hashlib.md5(vector.tobytes()).hexdigest()
    
    assert vector_database.data[vector_hash] == fact




def test_save_fact_invalid(vector_database):
    # Mockando um fato inválido
    vector_database.fact_checker.validate_input = MagicMock(return_value=False)
    fact = "Fake fact."

    # Tenta salvar o fato inválido
    result = vector_database.save_fact(fact)

    assert result is False
    assert vector_database.index.ntotal == 0  # Nenhum vetor foi adicionado


def test_is_valid_fact(vector_database):
    fact = "O céu é azul."

    # Mock de validação do fact_checker
    vector_database.fact_checker.validate_input = MagicMock(return_value=True)

    assert vector_database._is_valid_fact(fact) is True
