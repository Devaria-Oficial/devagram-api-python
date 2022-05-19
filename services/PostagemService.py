import os
from datetime import datetime

from bson import ObjectId

from models.UsuarioModel import UsuarioCriarModel, UsuarioAtualizarModel
from providers.AWSProvider import AWSProvider
from repositories.PostagemRepository import PostagemRepository

awsProvider = AWSProvider()
postagemRepository = PostagemRepository()


class PostagemService:

    async def cadastrar_postagem(self, postagem, usuario_id):
        try:
            postagem_criada = await postagemRepository.criar_postagem(postagem, usuario_id)

            try:
                caminho_foto = f'files/foto-{datetime.now().strftime("%H%M%S")}.png'

                with open(caminho_foto, 'wb+') as arquivo:
                    arquivo.write(postagem.foto.file.read())

                url_foto = awsProvider.upload_arquivo_s3(
                    f'fotos-postagem/{postagem_criada["id"]}.png',
                    caminho_foto
                )

                campo_atualizar = {
                    "foto": url_foto
                }
                nova_postagem = await postagemRepository.atualizar_postagem(postagem_criada["id"], campo_atualizar)

                os.remove(caminho_foto)
            except Exception as erro:
                print(erro)

            return {
                "mensagem": "Postagem criada com sucesso!",
                "dados": nova_postagem,
                "status": 201
            }

        except Exception as erro:
            print(erro)
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(erro),
                "status": 500
            }

    async def listar_postagens(self):
        try:
            postagens = await postagemRepository.listar_postagens()

            for p in postagens:
                p["total_curtidas"] = len(p["curtidas"])

            return {
                "mensagem": "Postagens listadas com sucesso!",
                "dados": postagens,
                "status": 200
            }
        except Exception as erro:
            print(erro)
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(erro),
                "status": 500
            }

    async def curtir_descurtir(self, postagem_id, usuario_id):
        try:
            postagem_encontrada = await postagemRepository.buscar_postagem(postagem_id)

            if postagem_encontrada["curtidas"].count(usuario_id) > 0:
                postagem_encontrada["curtidas"].remove(usuario_id)
            else:
                postagem_encontrada["curtidas"].append(ObjectId(usuario_id))

            postagem_atualizada = await postagemRepository.atualizar_postagem(postagem_encontrada["id"], {"curtidas": postagem_encontrada["curtidas"]})

            return {
                "mensagem": "Postagem curtida com sucesso!",
                "dados": postagem_atualizada,
                "status": 200
            }

        except Exception as erro:
            print(erro)
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(erro),
                "status": 500
            }

    async def criar_comentario(self, postagem_id, usuario_id, comentario):
        try:
            postagem_encontrada = await postagemRepository.buscar_postagem(postagem_id)

            postagem_encontrada["comentarios"].append({
                "usuario_id": ObjectId(usuario_id),
                "comentario": comentario
            })

            postagem_atualizada = await postagemRepository.atualizar_postagem(
                postagem_encontrada["id"],
                {"comentarios": postagem_encontrada["comentarios"]}
            )

            return {
                "mensagem": "Comentário criado com sucesso!",
                "dados": postagem_atualizada,
                "status": 200
            }

        except Exception as erro:
            print(erro)
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(erro),
                "status": 500
            }