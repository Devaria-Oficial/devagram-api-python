import os

from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile, Body
from datetime import datetime
from middlewares.JWTMiddleware import verificar_token
from models.ComentarioModel import ComentarioCriarModel, ComentarioAtualizarModel
from models.PostagemModel import PostagemCriarModel
from services.AuthService import AuthService
from services.UsuarioService import UsuarioService
from services.PostagemService import PostagemService

router = APIRouter()

usuarioService = UsuarioService()
postagemService = PostagemService()
authService = AuthService()

@router.post(
    "/",
    response_description="Rota para criar uma nova Postagem.",
    dependencies=[Depends(verificar_token)]
)
async def rota_criar_postagem(authorization: str = Header(default=''), postagem: PostagemCriarModel = Depends(PostagemCriarModel)):
    try:
        usuario_logado = await authService.buscar_usuario_logado(authorization)

        resultado = await postagemService.cadastrar_postagem(postagem, usuario_logado.id)

        if not resultado.status == 201:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as erro:
        raise erro


@router.get(
    '/',
    response_description='Rota para listar as Postagens.',
    dependencies=[Depends(verificar_token)]
    )
async def listar_postagens():
    try:
        resultado = await postagemService.listar_postagens()

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as erro:
        raise erro


@router.get(
    '/{usuario_id}',
    response_description='Rota para listar as Postagens de um usuário específico.',
    dependencies=[Depends(verificar_token)]
    )
async def listar_postagens_usuario(usuario_id: str):
    try:
        resultado = await postagemService.listar_postagens_usuario(usuario_id)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as erro:
        raise erro

@router.put(
    '/curtir/{postagem_id}',
    response_description="Rota para cutir/descurtir uma postagem",
    dependencies=[Depends(verificar_token)]
)
async def curtir_descurtir_postagem(postagem_id: str, authorization: str = Header(default='')):
    usuario_logado = await authService.buscar_usuario_logado(authorization)

    resultado = await postagemService.curtir_descurtir(postagem_id, usuario_logado.id)

    if not resultado.status == 200:
        raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

    return resultado


@router.put(
    '/comentar/{postagem_id}',
    response_description="Rota para criar um comentário em uma postagem",
    dependencies=[Depends(verificar_token)]
)
async def comentar_postagem(postagem_id: str, authorization: str = Header(default=''), comentario_model: ComentarioCriarModel = Body(...)):
    usuario_logado = await authService.buscar_usuario_logado(authorization)

    resultado = await postagemService.criar_comentario(postagem_id, usuario_logado.id, comentario_model.comentario)

    if not resultado.status == 200:
        raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

    return resultado


@router.delete(
    '/{postagem_id}/comentario/{comentario_id}',
    response_description="Rota para criar um comentário em uma postagem",
    dependencies=[Depends(verificar_token)]
)
async def deletar_comentario(postagem_id: str, comentario_id: str, authorization: str = Header(default='')):
    usuario_logado = await authService.buscar_usuario_logado(authorization)

    resultado = await postagemService.deletar_comentario(postagem_id, usuario_logado.id, comentario_id)

    if not resultado.status == 200:
        raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

    return resultado


@router.put(
    '/{postagem_id}/comentario/{comentario_id}',
    response_description="Rota para Atualizar um comentário em uma postagem",
    dependencies=[Depends(verificar_token)]
)
async def atualizar_comentario(postagem_id: str, comentario_id: str, authorization: str = Header(default=''), comentario_model: ComentarioAtualizarModel = Body(...)):
    usuario_logado = await authService.buscar_usuario_logado(authorization)

    resultado = await postagemService.atualizar_comentario(postagem_id, usuario_logado.id, comentario_id, comentario_model.comentario)

    if not resultado.status == 200:
        raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

    return resultado


@router.delete(
    '/{postagem_id}',
    response_description="Rota para deletar uma postagem.",
    dependencies=[Depends(verificar_token)]
)
async def deletar_postagem(postagem_id: str, authorization: str = Header(default='')):
    usuario_logado = await authService.buscar_usuario_logado(authorization)

    resultado = await postagemService.deletar_postagem(postagem_id, usuario_logado.id)

    if not resultado.status == 200:
        raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

    return resultado
