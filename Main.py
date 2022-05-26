from fastapi import FastAPI
from routes.UsuarioRoute import router as UsuarioRoute
from routes.AutenticacaoRoute import router as AutenticacaoRoute
from routes.PostagemRoute import router as PostagemRoute
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(UsuarioRoute, tags=["Usuário"], prefix="/api/usuario")
app.include_router(AutenticacaoRoute, tags=["Autenticação"], prefix="/api/auth")
app.include_router(PostagemRoute, tags=["Postagem"], prefix="/api/postagem")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["Health"])
async def health():
    return {
        "status": "OK!"
    }
