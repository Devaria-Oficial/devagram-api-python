from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthUtil:
    def gerar_senha_criptografada(self, senha):
        return pwd_context.hash(senha)

    def verificar_senha(self, senha, senha_criptografada):
        return pwd_context.verify(senha, senha_criptografada)