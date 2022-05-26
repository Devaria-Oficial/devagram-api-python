from pydantic import BaseModel, Field


class ComentarioModel(BaseModel):
    usuario_id: str = Field(...)
    comentario: str = Field(...)


class ComentarioCriarModel(BaseModel):
    comentario: str = Field(...)

class ComentarioAtualizarModel(BaseModel):
    comentario: str = Field(...)