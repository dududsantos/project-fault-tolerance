from fastapi import FastAPI, HTTPException
import random
import uuid
import time

app = FastAPI()

# Simulação de banco de dados para produtos e transações
products_db = {
    1: {"id": 1, "name": "Produto A", "value": 100.0},
    2: {"id": 2, "name": "Produto B", "value": 150.0},
    3: {"id": 3, "name": "Produto C", "value": 200.0},
}

transactions_log = []

@app.get("/product")
async def get_product(product: int):
    # Simular falha de omissão com 20% de probabilidade
    if random.random() < 0.2:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if product not in products_db:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return products_db[product]

@app.post("/sell")
async def sell_product(product: int):
    # Simular falha do tipo "Error" com 10% de probabilidade (Erro no processo de venda)
    if random.random() < 0.1:
        raise HTTPException(status_code=500, detail="Erro interno ao processar a venda")
    
    # Caso o produto seja vendido com sucesso
    transaction_id = str(uuid.uuid4())  # Gerar ID único para a transação
    transactions_log.append({"product": product, "transaction_id": transaction_id})
    
    return {"status": "success", "transaction_id": transaction_id}

@app.get("/failures")
async def get_failures():
    return {"transactions_log": transactions_log}
