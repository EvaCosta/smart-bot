
import logging
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import numpy as np
import os

logger = logging.getLogger(__name__)

class FactChecker:
    def __init__(self):
        # Carregar o modelo de embeddings para gerar representações semânticas
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.known_facts = [
            "A Terra é redonda.",
            "A água ferve a 100 graus Celsius.",
            "Os humanos possuem 23 pares de cromossomos."
        ]
        # Gerar embeddings dos fatos conhecidos
        self.known_facts_embeddings = self._generate_embeddings(self.known_facts)
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.knowledge_graph_url = 'https://kgsearch.googleapis.com/v1/entities:search'

    def _generate_embeddings(self, texts):
        return self.model.encode(texts, convert_to_tensor=True)

    def _compute_similarity(self, query_embedding):
        return cosine_similarity(query_embedding, self.known_facts_embeddings)

    def validate_input(self, user_input):
        # Gerar o embedding para a entrada do usuário
        user_input_embedding = self.model.encode([user_input], convert_to_tensor=True)
        similarities = self._compute_similarity(user_input_embedding)

        # Verificar se a entrada do usuário tem alta similaridade com algum fato conhecido
        if np.max(similarities) > 0.8:  # Limite de similaridade para considerar factual
            return True  # Fato verdadeiro
        else:
            return self._verify_with_google_knowledge_graph(user_input)

    def _verify_with_google_knowledge_graph(self, user_input):
        try:
            response = requests.get(f"{self.knowledge_graph_url}", params={"query": user_input, "key": self.google_api_key})
            data = response.json()

            item_list = data.get('itemListElement', [])
            if item_list:
                entity = item_list[0].get('result', {})
            else:
                entity = {}
            return entity
        except Exception as e:
            logger.error(f"Erro ao verificar com o Google Knowledge Graph: {e}")
            return {}