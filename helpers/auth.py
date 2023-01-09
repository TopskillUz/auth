import base64
import datetime
import json
import logging
import typing
import uuid
from datetime import timezone, timedelta

import jwt

from core.config import settings
from helpers.user import UserHelper


class AuthHelper:
    REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN
    ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
    JWT_ALGORITHM = settings.JWT_ALGORITHM
    JWT_PUBLIC_KEY = base64.b64decode(settings.JWT_PUBLIC_KEY).decode('utf-8')
    JWT_PRIVATE_KEY = base64.b64decode(settings.JWT_PRIVATE_KEY).decode('utf-8')

    @classmethod
    def _create_token(cls, subject: dict, expires_time: int):
        payload_data = {
            'iss': 'http://localhost:8000/',
            'sub': json.dumps(subject),
            # 'iat': datetime.datetime.now(tz=timezone.utc) + timedelta(minutes=expires_time),
            'exp': datetime.datetime.now(tz=timezone.utc) + timedelta(minutes=expires_time),
        }
        access_token = jwt.encode(
            payload=payload_data,
            key=cls.JWT_PRIVATE_KEY,
            algorithm=cls.JWT_ALGORITHM
        )
        return access_token

    @classmethod
    def create_access_token(cls, user_id: uuid.UUID, expires_time: int = ACCESS_TOKEN_EXPIRES_IN) -> str:
        return cls._create_token({'user_id': str(user_id), 'type': 'access'}, expires_time=expires_time)

    @classmethod
    def create_refresh_token(cls, user_id: uuid.UUID, expires_time: int = REFRESH_TOKEN_EXPIRES_IN) -> str:
        return cls._create_token({'user_id': str(user_id), 'type': 'refresh'}, expires_time=expires_time)

    @classmethod
    def _decode_token(cls, token: str) -> tuple[int, typing.Any]:
        try:
            decode_token = jwt.decode(token, cls.JWT_PUBLIC_KEY, algorithms=[cls.JWT_ALGORITHM])
            return 200, decode_token
        except jwt.ExpiredSignatureError:
            return 400, "Token expired. Get new one"
        except jwt.InvalidTokenError:
            return 400, "Invalid Token"
        except Exception as e:
            logging.error(str(e))
            return 500, "Internal server error"

    @classmethod
    async def refresh_token(cls, refresh_token: str) -> tuple[int, typing.Any]:
        status_code, result = cls._decode_token(token=refresh_token)
        if status_code == 200:
            try:
                subject = json.loads(result['sub'])
                if subject['type'] == 'refresh':
                    user_id = subject['user_id']
                    return 200, cls.create_access_token(user_id)
                else:
                    return 400, "Only refresh token is accepted"
            except Exception as e:
                logging.error(str(e))
                return 500, "Internal server error"
        else:
            return status_code, result

    @classmethod
    async def validate_access_token(cls, access_token: str) -> tuple[int, typing.Any]:
        status_code, result = cls._decode_token(token=access_token)
        if status_code == 200:
            try:
                subject = json.loads(result['sub'])
                if subject['type'] == 'access':
                    user_id = subject['user_id']
                    status_code, result = await UserHelper.get_user_by_id(id=user_id)
                    if status_code == 200:
                        if result.is_verified:
                            return status_code, result
                        else:
                            return 400, 'Please verify your account'
                    else:
                        return status_code, result
                else:
                    return 400, "Only access token is accepted"
            except Exception as e:
                logging.error(str(e))
                return 500, "Internal server error"
        else:
            return status_code, result
