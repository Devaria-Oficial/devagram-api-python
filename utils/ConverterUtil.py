class ConverterUtil:
    def usuario_converter(self, usuario):
        return {
            "id": str(usuario["_id"]),
            "nome": usuario["nome"],
            "email": usuario["email"],
            "senha": usuario["senha"],
            "foto": usuario["foto"] if "foto" in usuario else ""
        }

    def postagem_converter(self, postagem):
        return {
            "id": str(postagem["_id"]) if "_id" in postagem else "",
            "usuario_id": str(postagem["usuario_id"]) if "usuario_id" in postagem else "",
            "foto": postagem["foto"] if "foto" in postagem else "",
            "legenda": postagem["legenda"] if "legenda" in postagem else "",
            "data": postagem["data"] if "data" in postagem else "",
            "curtidas": [str(p) for p in postagem["curtidas"]] if "curtidas" in postagem else "",
            "comentarios": [str(p) for p in postagem["comentarios"]] if "comentarios" in postagem else "",
            "usuario": self.usuario_converter(postagem["usuario"][0]) if "usuario" in postagem and len(postagem["usuario"]) > 0 else ""
        }