import motor.motor_asyncio

from bson import ObjectId
from decouple import config
from models.PostagemModel import PostagemCriarModel

MONGODB_URL = config("MONGODB_URL")

cliente = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = cliente.devagram

postagem_collection = database.get_collection("postagem")


def postagem_helper(postagem):
    return {
        "id": str(postagem["_id"]) if "_id" in postagem else "",
        "usuario": postagem["usuario"] if "usuario" in postagem else "",
        "foto": postagem["foto"] if "foto" in postagem else "",
        "legenda": postagem["legenda"] if "legenda" in postagem else "",
        "data": postagem["data"] if "data" in postagem else "",
        "curtidas": postagem["curtidas"] if "curtidas" in postagem else "",
        "comentarios": postagem["comentarios"] if "comentarios" in postagem else "",
    }


async def criar_postagem(postagem: PostagemCriarModel) -> dict:
    postagem_criada = await postagem_collection.insert_one(postagem.__dict__)

    nova_postagem = await postagem_collection.find_one({ "_id": postagem_criada.inserted_id })

    return postagem_helper(nova_postagem)


async def listar_postagens():
    return postagem_collection.find()


async def buscar_postagem(id: str) -> dict:
    postagem = await postagem_collection.find_one({"_id": ObjectId(id)})

    if postagem:
        return postagem_helper(postagem)


async def deletar_postagem(id: str):
    postagem = await postagem_collection.find_one({"_id": ObjectId(id)})

    if postagem:
        await postagem_collection.delete_one({"_id": ObjectId(id)})