# Usar uma imagem base do Python
FROM python:3.10-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar apenas os arquivos essenciais para instalar dependências
COPY requirements.txt .

RUN pip install --upgrade pip

# Instalar dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código para o container
COPY . .

# Definir variáveis de ambiente (opcional)
ENV PYTHONUNBUFFERED=1

# Expor a porta utilizada pelo Streamlit
EXPOSE 8501

# Comando para iniciar a aplicação
CMD ["streamlit", "run", "app/ui.py"]
