from fastapi import FastAPI, HTTPException
import random
import time

app = FastAPI()

# Variável para armazenar a última taxa de câmbio válida
last_valid_exchange_rate = 1.0  # Valor inicial padrão

@app.get("/exchange")
async def get_exchange_rate():
    global last_valid_exchange_rate

    # Simular falha do tipo Crash com 10% de probabilidade
    if random.random() < 0.1:
        raise HTTPException(status_code=503, detail="Service crashed")

    try:
        # Simular cálculo da taxa de câmbio
        exchange_rate = random.uniform(0.5, 1.5)

        # Armazenar a taxa de câmbio como última válida
        last_valid_exchange_rate = exchange_rate

        return {"exchange_rate": exchange_rate}

    except Exception as e:
        # Usar a última taxa válida em caso de erro
        return {"exchange_rate": last_valid_exchange_rate, "error": str(e)}
