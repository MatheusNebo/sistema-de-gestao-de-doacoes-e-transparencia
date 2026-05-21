from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.system_user_repository import UserRepository
from app.schemas.system_user_schema import UserCreate, UserUpdate
from fastapi import HTTPException, status

# configuração para hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    async def create_user(self, db: AsyncSession, user_data: UserCreate):
        # verifica se email ou username já existem
        existing_user = await self.repository.get_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")

        # transforma os dados e fazer o Hash da senha
        user_dict = user_data.model_dump()
        user_dict["password"] = self.get_password_hash(user_dict["password"])

        # salva no banco
        async with db.begin():
            new_user = await self.repository.create(db, user_dict)
            return new_user

    async def list_users(self, db: AsyncSession):
        return await self.repository.get_all(db)

    async def get_user_by_id(self, db: AsyncSession, user_id: int):
        user = await self.repository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        return user