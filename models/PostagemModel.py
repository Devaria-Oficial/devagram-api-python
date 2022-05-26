from fastapi import UploadFile
from pydantic import BaseModel, Field
from typing import List, Optional
from utils.DecoratorUtil import DecoratorUtil
from models.UsuarioModel import UsuarioModel

decoratorUtil = DecoratorUtil()


class PostagemModel(BaseModel):
    id: str = Field(...)
    usuario_id: str = Field(...)
    foto: str = Field(...)
    legenda: str = Field(...)
    data: str
    curtidas: List
    comentarios: List
    usuario: Optional[UsuarioModel]
    total_curtidas: int
    total_comentarios: int

    def __getitem__(self, item):
        return getattr(self, item)

    class Config:
        schema_extra = {
            "postagem": {
                "id": "string",
                "foto": "string",
                "legenda": "string",
                "data": "date",
                "curtidas": "int",
                "comentarios": "List[comentarios]"
            }
        }


@decoratorUtil.form_body
class PostagemCriarModel(BaseModel):
    foto: UploadFile = Field(...)
    legenda: str = Field(...)

    class Config:
        schema_extra = {
            "postagem": {
                "foto": "string",
                "legenda": "string",
            }
        }