import logging
import faiss
import hashlib
from app.fact_checker import FactChecker
import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class VectorDatabase:
    def __init__(self):
        self.index = faiss.IndexFlatL2(384)  # Dimensão do vetor do modelo de embeddings
        self.data = {}
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Modelo de embeddings
        self.fact_checker = FactChecker()  # Instanciando o FactChecker corretamente

    def save(self, question, response):
        vector = self._embed(question)
        self.index.add(np.array([vector]))
        vector_hash = hashlib.md5(vector.tobytes()).hexdigest()  # Gera um hash único para o vetor
        self.data[vector_hash] = response

    def query(self, question):
        vector = self._embed(question)
        D, I = self.index.search(np.array([vector]), 1)
        if D[0][0] < 0.1:
            # Use o hash do vetor para buscar no dicionário
            vector_hash = hashlib.md5(vector.tobytes()).hexdigest()
            return self.data.get(vector_hash)
        return None

    def save_fact(self, fact):
        # Validação do fato antes de ser armazenado
        if self._is_valid_fact(fact):
            vector = self._embed(fact)  # Gera o vetor
            vector_hash = hashlib.md5(vector.tobytes()).hexdigest()  # Gera o hash único
            self.index.add(np.array([vector]))
            self.data[vector_hash] = fact  # Salva o fato usando o hash
            logger.info(f"Fato armazenado: {fact}")
            return True
        else:
            logger.warning(f"Fato inválido, não armazenado: {fact}")
            return False

    def _is_valid_fact(self, fact):
        # Validação de fato, agora com o fact_checker corretamente instanciado
        return self.fact_checker.validate_input(fact)

    def _embed(self, text):
        # Gera embeddings consistentes como array NumPy (float32)
        return self.model.encode(text, convert_to_numpy=True).astype('float32')

