from fastapi import UploadFile
from pydantic import BaseModel, Field
from typing import List
from utils.DecoratorUtil import DecoratorUtil
from models.UsuarioModel import UsuarioModel

decoratorUtil = DecoratorUtil()


class PostagemModel(BaseModel):
    id: str = Field(...)
    usuario: UsuarioModel = Field(...)
    foto: str = Field(...)
    legenda: str = Field(...)
    data: str = Field(...)
    curtidas: int = Field(...)
    comentarios: List = Field(...)

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