from fastapi import APIRouter, Body, HTTPException

from models.UsuarioModel import UsuarioLoginModel
from services.AuthService import AuthService

router = APIRouter()

authService = AuthService()


@router.post('/login')
async def login(usuario: UsuarioLoginModel = Body(...)):
    resultado = await authService.login_service(usuario)

    if not resultado.status == 200:
        raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

    del resultado.dados.senha

    token = authService.gerar_token_jwt(resultado.dados.id)

    resultado.dados.token = token

    return resultado