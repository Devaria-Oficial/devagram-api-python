from fastapi import APIRouter, Body, HTTPException

from models.UsuarioModel import UsuarioCriarModel
from services.UsuarioService import (
    registrar_usuario
)

router = APIRouter()


@router.post("/", response_description="Rota para criar um novo Usuário.")
async def rota_criar_usuario(usuario: UsuarioCriarModel = Body(...)):
    try:
        resultado = await registrar_usuario(usuario)

        if not resultado['status'] == 201:
            raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])

        return resultado
    except Exception as erro:
        print(erro)

        return {
            "mensagem": "Erro interno no servidor."
        }
