from typing import List

from fastapi import Form, UploadFile
from pydantic import BaseModel, Field, EmailStr
from utils.DecoratorUtil import DecoratorUtil

decoratorUtil = DecoratorUtil()


class UsuarioModel(BaseModel):
    id: str = Field(...)
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    foto: str = Field(...)
    seguidores: List
    seguindo: List
    total_seguidores: int
    total_seguindo: int
    postagens: List
    total_postagem: int
    token: str

    def __getitem__(self, item):
        return getattr(self, item)

    class Config:
        schema_extra = {
            "usuario": {
                "nome": "string",
                "email": "string",
                "senha": "string",
                "foto": "string",
                "seguidores": "List",
                "seguindo": "List"
            }
        }


@decoratorUtil.form_body
class UsuarioCriarModel(BaseModel):
    nome: str = Field(max_length=50, min_length=3)
    email: EmailStr = Field(...)
    senha: str = Field(...)

    class Config:
        schema_extra = {
            "usuario": {
                "nome": "Fulano de tal",
                "email": "fulano@gmail.com",
                "senha": "SeNha123!",
            }
        }


class UsuarioLoginModel(BaseModel):
    email: EmailStr = Field(...)
    senha: str = Field(...)

    class Config:
        schema_extra = {
            "usuario": {
                "email": "fulano@gmail.com",
                "senha": "SeNha123!",
            }
        }


@decoratorUtil.form_body
class UsuarioAtualizarModel(BaseModel):
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    foto: UploadFile = Field(...)

    class Config:
        schema_extra = {
            "usuario": {
                "nome": "Fulano de tal",
                "email": "fulano@gmail.com",
                "senha": "SeNha123!",
            }
        }