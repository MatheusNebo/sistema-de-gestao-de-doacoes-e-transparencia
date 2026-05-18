from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.system_user import User  # Supondo que seu model se chame User

class UserRepository:

    async def create(self, db: AsyncSession, user_data: dict):
        # cria um novo usuário a partir de um dicionário (já com hash de senha)
        user = User(**user_data)
        db.add(user)
        await db.flush() # envia para o banco para gerar o ID, mas aguarda o commit do Service
        await db.refresh(user)
        return user

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(User))
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, user_id: int):
        result = await db.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, db: AsyncSession, email: str):
        # busca usuário pelo e-mail. 
        # importante para o Login e para evitar duplicidade no cadastro.

        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(self, db: AsyncSession, username: str):
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def update(self, db: AsyncSession, user_id: int, update_data: dict):
        # atualiza dados do usuário dinamicamente.
        user = await self.get_by_id(db, user_id)
        if not user:
            return None
        
        for key, value in update_data.items():
            if value is not None:
                setattr(user, key, value)
        
        await db.flush()
        return user