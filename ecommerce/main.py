from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import requests
import uuid
import logging

app = FastAPI()

# URLs dos serviços externos
STORE_URL = "http://store:8001"
EXCHANGE_URL = "http://exchange:8002"
FIDELITY_URL = "http://fidelity:8003"

# Última taxa de conversão válida
last_exchange_rate = 1.0

# Configuração de logging
logging.basicConfig(level=logging.INFO, filename="ecommerce.log", filemode="a")

# Modelo de dados para o request do endpoint "buy"
class BuyRequest(BaseModel):
    product: int
    user: int
    ft: bool

# Endpoint principal
@app.post("/buy")
async def buy(request: BuyRequest):
    global last_exchange_rate

    try:
        # Request 1: Consultar informações do produto
        product_data = await get_product_data(request.product, request.ft)

        # Request 2: Consultar taxa de câmbio
        exchange_rate = await get_exchange_rate(request.ft)

        # Request 3: Registrar a venda
        transaction_id = await register_sale(request.product, request.ft)

        # Request 4: Registrar bônus
        bonus = round(product_data["value"])
        await register_bonus(request.user, bonus, request.ft)

        return {"status": "success", "transaction_id": transaction_id}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Tolerância a falhas nos serviços externos
async def get_product_data(product, ft):
    if ft:
        try:
            response = requests.get(
                f"{STORE_URL}/product?product={product}",
                timeout=1
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            raise HTTPException(status_code=503, detail="Falha ao consultar o Store.")
    else:
        return {"id": product, "name": "Produto Padrão", "value": 100.0}


async def get_exchange_rate(ft):
    global last_exchange_rate
    if ft:
        try:
            response = requests.get(f"{EXCHANGE_URL}/exchange", timeout=1)
            response.raise_for_status()
            last_exchange_rate = response.json().get("exchange_rate", 1.0)
            return last_exchange_rate
        except requests.exceptions.RequestException:
            return last_exchange_rate
    else:
        return last_exchange_rate


async def register_sale(product, ft):
    if ft:
        try:
            response = requests.post(
                f"{STORE_URL}/sell",
                json={"product": product},
                timeout=1
            )
            response.raise_for_status()
            return response.json().get("transaction_id", str(uuid.uuid4()))
        except requests.exceptions.RequestException:
            raise HTTPException(status_code=503, detail="Falha ao registrar a venda no Store.")
    else:
        return str(uuid.uuid4())


async def register_bonus(user, bonus, ft):
    if ft:
        try:
            response = requests.post(
                f"{FIDELITY_URL}/bonus",
                json={"user": user, "bonus": bonus},
                timeout=1
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Falha ao registrar bônus para o usuário {user}. Erro: {e}")
            # Não interromper o fluxo de compra mesmo que ocorra falha aqui
    else:
        logging.info(f"Bônus não registrado para o usuário {user}. Valor: {bonus}.")
