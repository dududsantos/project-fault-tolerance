# Guia para Executar o Sistema de Tolerância a Falhas

Este projeto consiste em um sistema distribuído com tolerância a falhas, utilizando microsserviços em contêineres Docker.

## Requisitos

- Python 3.8 ou superior
- Docker e Docker Compose
- Postman ou ferramenta similar para testes de API

## Configuração do Ambiente

1. **Clone o repositório**:

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_DIRETORIO>
   ```

2. **Crie um ambiente virtual (venv)**:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/MacOS
   venv\Scripts\activate    # Windows
   ```

3. **Instale as dependências**:
   Cada microsserviço possui um arquivo `requirements.txt`. Navegue até o diretório de cada um e execute:
   ```bash
   pip install -r requirements.txt
   ```

## Executando o Sistema

1. **Construa e inicie os contêineres Docker**:
   Certifique-se de estar no diretório raiz do projeto (onde está localizado o arquivo `docker-compose.yml`) e execute:

   ```bash
   docker-compose up --build
   ```

2. **Verifique se os contêineres estão em execução**:
   ```bash
   docker ps
   ```
   Todos os microsserviços devem estar listados.

## Testando os Endpoints

Utilize o Postman ou outra ferramenta similar para testar os endpoints descritos na especificação:

- **E-commerce (porta 8000)**:

  - POST `/buy`

- **Store (porta 8001)**:

  - GET `/product`
  - POST `/sell`

- **Exchange (porta 8002)**:

  - GET `/exchange`

- **Fidelity (porta 8003)**:
  - POST `/bonus`

Os exemplos de requisições estão descritos no código e no relatório.

## Parar o Sistema

Para encerrar todos os contêineres, execute:

```bash
docker-compose down
```

