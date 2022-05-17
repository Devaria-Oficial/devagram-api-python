from fastapi import APIRouter, Body, HTTPException

from models.UsuarioModel import UsuarioLoginModel
from services.AuthService import login_service, gerar_token_jwt

router = APIRouter()


@router.post('/login')
async def login(usuario: UsuarioLoginModel = Body(...)):
    resultado = await login_service(usuario)


    if not resultado['status'] == 200:
        raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])

    del resultado['dados']['senha']

    token = gerar_token_jwt(resultado['dados']['id'])

    resultado['dados']['token'] = token

    return resultado