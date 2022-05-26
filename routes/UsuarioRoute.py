import os

from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile
from datetime import datetime
from middlewares.JWTMiddleware import verificar_token
from models.UsuarioModel import UsuarioCriarModel, UsuarioAtualizarModel
from services.AuthService import AuthService
from services.UsuarioService import UsuarioService

router = APIRouter()

usuarioService = UsuarioService()
authService = AuthService()


@router.post("/", response_description="Rota para criar um novo Usuário.")
async def rota_criar_usuario(file: UploadFile, usuario: UsuarioCriarModel = Depends(UsuarioCriarModel)):
    try:
        caminho_foto = f'files/foto-{datetime.now().strftime("%H%M%S")}.png'

        with open(caminho_foto, 'wb+') as arquivo:
            arquivo.write(file.file.read())

        resultado = await usuarioService.registrar_usuario(usuario, caminho_foto)

        os.remove(caminho_foto)

        if not resultado.status == 201:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as erro:
        raise erro


@router.get(
    '/me',
    response_description='Rota para buscar as informações do usuário logado.',
    dependencies=[Depends(verificar_token)]
    )
async def buscar_info_usuario_logado(authorization: str = Header(default='')):
    try:
        usuario_logado = await authService.buscar_usuario_logado(authorization)

        resultado = await usuarioService.buscar_usuario(usuario_logado.id)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as erro:
        raise erro


@router.get(
    '/{usuario_id}',
    response_description='Rota para buscar as informações do usuário logado.',
    dependencies=[Depends(verificar_token)]
    )
async def buscar_info_usuario(usuario_id: str):
    try:
        resultado = await usuarioService.buscar_usuario(usuario_id)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as erro:
        raise erro


@router.get(
    '/',
    response_description='Rota para listar todos usuários.',
    dependencies=[Depends(verificar_token)]
    )
async def listar_usuarios(nome: str):
    try:
        resultado = await usuarioService.listar_usuarios(nome)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as erro:
        raise erro


@router.put(
    '/me',
    response_description='Rota para atualizar as informações do usuário logado.',
    dependencies=[Depends(verificar_token)]
    )
async def atualizar_usuario_logado(authorization: str = Header(default=''), usuario_atualizar: UsuarioAtualizarModel = Depends(UsuarioAtualizarModel)):
    try:
        usuario_logado = await authService.buscar_usuario_logado(authorization)

        resultado = await usuarioService.atualizar_usuario_logado(usuario_logado.id, usuario_atualizar)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as erro:
        raise erro

@router.put(
    '/seguir/{usuario_id}',
    response_description="Rota para follow/unfollow em um usuário.",
    dependencies=[Depends(verificar_token)]
)
async def follow_unfollow_usuario(usuario_id: str, authorization: str = Header(default='')):
    usuario_logado = await authService.buscar_usuario_logado(authorization)

    resultado = await usuarioService.follow_unfollow_usuario(usuario_logado.id, usuario_id)

    if not resultado.status == 200:
        raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

    return resultado
