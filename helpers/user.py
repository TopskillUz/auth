import logging
import typing
import uuid

from sqlalchemy import select

from core import utils
from core.database import get_session

from models.user import User


class UserHelper:
    @classmethod
    async def check_email_exists(cls, email: str) -> tuple[int, typing.Any]:
        try:
            async with get_session() as db:
                query = select(User).where(User.email == email)
                users = await db.execute(query)
                result = users.first()
                if bool(result):
                    return 200, result[0]
                else:
                    return 404, "User not found!"
        except Exception as e:
            logging.info(e)
            return 500, "Internal server error"

    @classmethod
    async def check_phone_exists(cls, phone: str) -> tuple[int, typing.Any]:
        try:
            async with get_session() as db:
                query = select(User).where(User.phone == phone)
                users = await db.execute(query)
                result = users.first()
                if bool(result):
                    return 200, result[0]
                else:
                    return 404, "User not found!"
        except Exception as e:
            logging.info(e)
            return 500, "Internal server error"

    @classmethod
    async def get_user_by_id(cls, id: typing.Union[uuid.UUID, str]):
        try:
            async with get_session() as db:
                query = select(User).where(User.id == id)
                users = await db.execute(query)
                result = users.first()
                if bool(result):
                    return 200, result[0]
                else:
                    return 404, "User not found!"
        except Exception as e:
            logging.info(e)
            return 500, "Internal server error"

    @classmethod
    async def register_user(cls, email: str, phone: str, password: str, last_name: str, first_name: str,
                            middle_name: str) -> tuple[int, typing.Any]:
        status_code, result = await UserHelper.check_email_exists(email=email)
        if status_code != 200:
            status_code, result = await UserHelper.check_phone_exists(phone=phone)
            if status_code != 200:
                try:
                    async with get_session() as db:
                        password = utils.hash_password(password=password)
                        user = User(email=email, password=password, phone=phone, last_name=last_name,
                                    first_name=first_name, middle_name=middle_name)
                        db.add(user)
                        try:
                            await db.commit()
                            await db.refresh(user)
                            return 200, user
                        except Exception as e:
                            logging.error(e)
                            await db.rollback()
                            return 500, "Internal server error"
                except Exception as e:
                    logging.info(e)
                    return 500, "Internal server error"
            else:
                return 400, 'This phone already stored'
        else:
            return 400, 'This email already stored'

    @classmethod
    async def login(cls, email: str, password: str) -> tuple[int, typing.Any]:
        from helpers.auth import AuthHelper
        status_code, result = await UserHelper.check_email_exists(email=email)
        if status_code == 200:
            if utils.verify_password(password, result.password):
                access_token = AuthHelper.create_access_token(user_id=result.id)
                refresh_token = AuthHelper.create_refresh_token(user_id=result.id)
                return 200, {"access_token": access_token, "refresh_token": refresh_token}
            else:
                return 403, "Invalid credentials"
        else:
            return 403, "Invalid credentials"
