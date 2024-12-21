from fastapi import FastAPI, HTTPException
import random
import time

app = FastAPI()

# Variável para armazenar um log das falhas no Fidelity
failure_log = []

@app.post("/bonus")
async def register_bonus(user: int, bonus: int):
    global failure_log

    # Simular falha do tipo "Time" com 10% de probabilidade
    if random.random() < 0.1:
        raise HTTPException(status_code=504, detail="Timeout error")

    try:
        # Simular o processo de registro do bônus
        if random.random() < 0.2:  # Simula uma falha com 20% de probabilidade
            raise ValueError("Falha interna ao registrar bônus")

        # Caso o bônus seja registrado com sucesso
        return {"status": "success", "user": user, "bonus": bonus}

    except Exception as e:
        # Em caso de falha, logar a falha e retornar uma resposta com o erro
        failure_log.append({"user": user, "bonus": bonus, "error": str(e)})
        
        # A operação será registrada no log e processada posteriormente
        return {"status": "failure", "message": "Falha registrada, será processada quando possível", "error": str(e)}

@app.get("/failures")
async def get_failures():
    return {"failures": failure_log}
