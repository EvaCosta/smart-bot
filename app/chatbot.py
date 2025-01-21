import logging
from app.langchain_api import LangChainAPI
from app.vector_database import VectorDatabase
from app.fact_checker import FactChecker
from app.user_preferences import UserPreferences
import sys 

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Chatbot:
    def __init__(self):
        self.api = LangChainAPI()
        self.db = VectorDatabase()
        self.fact_checker = FactChecker()
        self.preferences = UserPreferences()

    def respond(self, user_input, user_id=None):
        logger.debug(f"User input: {user_input}")
        
        if not self._is_valid_input(user_input):
            return "Entrada inválida, por favor tente novamente."
        
        # Verifica se já existe uma resposta no banco de dados
        existing_response = self.db.query(user_input)
        if existing_response:
            logger.info("Resposta existente encontrada.")
            return existing_response  # Retorna a resposta existente diretamente

        try:
            # Valida a entrada antes de armazenar
            if self.fact_checker.validate_input(user_input):
                self.db.save_fact(user_input)  # Armazena o novo fato no banco de dados
                logger.info(f"Fato válido armazenado: {user_input}")
            
            response = self.api.generate_response(user_input, user_id, self.preferences.get_preference(user_id))  # Ajuste o tom da resposta
            self.db.save(user_input, response)  # Salva a nova resposta no banco de dados

            return response
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {e}")
            return "Erro ao gerar resposta. Tente novamente mais tarde."

    def _is_valid_input(self, user_input):
        user_input = user_input.strip()
        if len(user_input) <= 3:
            return False
        if user_input.isdigit():  # Verifica se é apenas numérico
            return False
        if not any(char.isalpha() for char in user_input):  # Pelo menos uma letra
            return False
        return True