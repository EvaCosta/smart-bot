import os
import logging
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

logger = logging.getLogger(__name__)

class LangChainAPI:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY não configurada. Verifique o arquivo .env.")
        self.client = Groq(api_key=self.api_key)

    def generate_response(self, prompt, user_id=None, tone="informal"):
        logger.debug(f"Gerando resposta para o prompt: {prompt}")
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",  
                messages=[{"role": "user", "content": prompt}],
                temperature=1,
                max_completion_tokens=1024,
                top_p=1,
                stream=True,
            )
            response = ""
            for chunk in completion:
                response += chunk.choices[0].delta.content or ""

            # Ajuste de tom dependendo da preferência do usuário
            if tone == "formal":
                response = self._make_formal(response)
            return response
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {e}")
            return f"Erro ao gerar resposta: {e}"

    def _make_formal(self, response):
        # Método para ajustar o tom para formal
        return f"Prezado usuário, {response}"