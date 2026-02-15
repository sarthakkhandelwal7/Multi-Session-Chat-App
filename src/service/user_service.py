from src.db.db_adapter import DatabaseAdapter
from src.core import Settings
from src.db.schema import User
from sqlalchemy import select, delete, update
import logging
from typing import Optional, List


class UserService:
    def __init__(self, db: DatabaseAdapter, settings: Settings):
        self.db = db
        self.settings = settings

    async def create_user(self, first_name: str, last_name: str, email: str) -> dict:
        """Create a new user"""
        try:
            response = await self.db.insert_rows(
                table_model=User,
                query_type="Create user",
                rows=[
                    {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                    }
                ],
                returning=[User.user_id],
            )
            return response[0]
        except Exception as e:
            logging.error(f"Error creating user: {e}")
            raise e

    async def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Get user by ID"""
        try:
            query = select(User).where(User.user_id == user_id)
            result = await self.db.execute_query(query)
            return result[0] if result else None
        except Exception as e:
            logging.error(f"Error fetching user: {e}")
            raise e

    async def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get user by email"""
        try:
            query = select(User).where(User.email == email)
            result = await self.db.execute_query(query)
            return result[0] if result else None
        except Exception as e:
            logging.error(f"Error fetching user by email: {e}")
            raise e

    async def get_all_users(self) -> List[dict]:
        """Get all users"""
        try:
            query = select(User).order_by(User.created_at.desc())
            return await self.db.execute_query(query)
        except Exception as e:
            logging.error(f"Error fetching all users: {e}")
            raise e

    async def update_user(
        self,
        user_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
    ) -> dict:
        """Update user information"""
        try:
            update_data = {}
            if first_name is not None:
                update_data[User.first_name] = first_name
            if last_name is not None:
                update_data[User.last_name] = last_name
            if email is not None:
                update_data[User.email] = email

            if not update_data:
                user = await self.get_user_by_id(user_id)
                return user

            stmt = update(User).where(User.user_id == user_id).values(**update_data)
            await self.db.execute_query(stmt)
            return await self.get_user_by_id(user_id)
        except Exception as e:
            logging.error(f"Error updating user: {e}")
            raise e

    async def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        try:
            stmt = delete(User).where(User.user_id == user_id)
            await self.db.execute_query(stmt)
            return True
        except Exception as e:
            logging.error(f"Error deleting user: {e}")
            raise e
