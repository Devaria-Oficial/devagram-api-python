import time

import jwt
from decouple import config

from dtos.ResponseDTO import ResponseDTO
from models.UsuarioModel import UsuarioLoginModel, UsuarioModel
from repositories.UsuarioRepository import UsuarioRepository
from services.UsuarioService import UsuarioService
from utils.AuthUtil import AuthUtil

JWT_SECRET = config('JWT_SECRET')

usuarioRepository = UsuarioRepository()

authUtil = AuthUtil()

usuarioService = UsuarioService()


class AuthService:

    def gerar_token_jwt(self, usuario_id: str) -> str:
        payload = {
            "usuario_id": usuario_id,
            "tempo_expiracao": time.time() + 6000
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

        return token

    def decodificar_token_jwt(self, token: str):
        try:
            token_decodificado = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

            if token_decodificado["tempo_expiracao"] >= time.time():
                return token_decodificado
            else:
                return None
        except Exception as erro:
            print(erro)
            return None

    async def login_service(self, usuario: UsuarioLoginModel):
        usuario_encontrado = await usuarioRepository.buscar_usuario_por_email(usuario.email)

        if not usuario_encontrado:
            return ResponseDTO("E-mail ou Senha incorretos.", "", 401)
        else:
            if authUtil.verificar_senha(usuario.senha, usuario_encontrado.senha):
                return ResponseDTO("Login realizado com sucesso!", usuario_encontrado, 200)
            else:
                return ResponseDTO("E-mail ou Senha incorretos.", "", 401)

    async def buscar_usuario_logado(self, authorization: str) -> UsuarioModel:
        token = authorization.split(' ')[1]
        payload = self.decodificar_token_jwt(token)

        resultado_usuario = await usuarioService.buscar_usuario(payload["usuario_id"])


        usuario_logado = resultado_usuario.dados

        return usuario_logado