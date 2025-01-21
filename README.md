
# Smart Bot - Documentação de Execução Local

## Pré-requisitos

- **Python 3.10+**
- **Docker** (opcional)

## Passos de Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/EvaCosta/smart-bot.git
   cd smart-bot
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Executando a Aplicação

### Com Docker:

1. Construa e inicie os containers:
   ```bash
   docker-compose up --build
   ```

1. Testes
   ```bash
   docker-compose run test
   ```
### Sem Docker:

1. Execute a aplicação:
   ```bash
   python app/main.py
   ```

## Testes

Para rodar os testes:
```bash
pytest
```

## Exemplos de Uso

Após iniciar o bot, acesse no navegador:
```
http://localhost:8501
```

## Configurações

Crie um arquivo `.env` com as variáveis necessárias:
```
API_KEY=your_api_key
DATABASE_URL=your_database_url
```
