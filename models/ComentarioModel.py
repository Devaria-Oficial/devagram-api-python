from pydantic import BaseModel, Field

from models import UsuarioModel


class ComentarioModel(BaseModel):
    usuario: UsuarioModel = Field(...)
    comentario: str = Field(...)

    