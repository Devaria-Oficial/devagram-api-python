from models.PostagemModel import PostagemModel
from models.UsuarioModel import UsuarioModel


class ConverterUtil:
    def usuario_converter(self, usuario):
        return UsuarioModel(
            id=str(usuario["_id"]),
            nome=usuario["nome"],
            email=usuario["email"],
            senha=usuario["senha"],
            foto=usuario["foto"] if "foto" in usuario else "",
            seguidores=[str(p) for p in usuario["seguidores"]] if "seguidores" in usuario else [],
            seguindo=[str(p) for p in usuario["seguindo"]] if "seguindo" in usuario else [],
            total_seguidores= usuario["total_seguidores"] if "total_seguidores" in usuario else 0,
            total_seguindo=usuario["total_seguindo"] if "total_seguindo" in usuario else 0,
            postagens=usuario["postagens"] if "postagens" in usuario else [],
            total_postagem=usuario["total_postagem"] if "total_postagem" in usuario else 0,
            token=usuario["token"] if "token" in usuario else "",
        )

    def postagem_converter(self, postagem):
        return PostagemModel(
            id=str(postagem["_id"]) if "_id" in postagem else "",
            usuario_id=str(postagem["usuario_id"]) if "usuario_id" in postagem else "",
            foto=postagem["foto"] if "foto" in postagem else "",
            legenda=postagem["legenda"] if "legenda" in postagem else "",
            data=str(postagem["data"]) if "data" in postagem else "",
            curtidas=[str(p) for p in postagem["curtidas"]] if "curtidas" in postagem else [],
            comentarios=[
                {
                    "comentario": p["comentario"],
                    "comentario_id": str(p["comentario_id"]),
                    "usuario_id": str(p["usuario_id"])
                } for p in postagem["comentarios"]
            ] if "comentarios" in postagem else "",
            usuario=self.usuario_converter(postagem["usuario"][0]) if "usuario" in postagem and len(postagem["usuario"])>0 else None,
            total_curtidas=postagem["total_curtidas"] if "total_curtidas" in postagem else 0,
            total_comentarios=postagem["total_comentarios"] if "total_comentarios" in postagem else 0,
        )
