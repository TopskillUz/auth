import asyncio
import logging

from grpc import aio

from grpc_generated_files import auth_pb2_grpc, auth_pb2
from helpers.auth import AuthHelper
from helpers.user import UserHelper


class AuthServicer(auth_pb2_grpc.AuthServiceServicer):

    async def register(self, request, context):
        print("AuthServicer received request from GatewayClient")
        status_code, result = await UserHelper.register_user(email=request.email, password=request.password,
                                                             phone=request.phone, last_name=request.last_name,
                                                             first_name=request.first_name,
                                                             middle_name=request.middle_name)
        if status_code == 200:
            user = auth_pb2.User(id=str(result.id), email=result.email, phone=result.phone,
                                 last_name=result.last_name, first_name=result.first_name,
                                 middle_name=result.middle_name)
            response = auth_pb2.RegisterUserResponse(
                success_payload=user,
                error=False,
                status_code=status_code,
            )
            return response
        else:
            response = auth_pb2.RegisterUserResponse(
                error_payload=result,
                error=True,
                status_code=status_code
            )
            return response

    async def login(self, request, context):
        print("AuthServicer received request from GatewayClient")
        status_code, result = await UserHelper.login(email=request.email, password=request.password)
        if status_code == 200:
            tokens = auth_pb2.TokenSchema(access_token=result['access_token'], refresh_token=result['refresh_token'], )
            response = auth_pb2.LoginResponse(
                success_payload=tokens,
                error=False,
                status_code=status_code,
            )
            return response
        else:
            response = auth_pb2.LoginResponse(
                error_payload=result,
                error=True,
                status_code=status_code
            )
            return response

    async def refresh_token(self, request, context):
        print("AuthServicer received request from GatewayClient")
        status_code, result = await AuthHelper.refresh_token(refresh_token=request.refresh_token)
        if status_code == 200:
            tokens = auth_pb2.TokenSchema(access_token=result)
            response = auth_pb2.RefreshTokenResponse(
                success_payload=tokens,
                error=False,
                status_code=status_code,
            )
            return response
        else:
            response = auth_pb2.RefreshTokenResponse(
                error_payload=result,
                error=True,
                status_code=status_code
            )
            return response

    async def validate_access_token(self, request, context):
        print("AuthServicer received request from GatewayClient")
        status_code, result = await AuthHelper.validate_access_token(access_token=request.access_token)
        if status_code == 200:
            user = auth_pb2.User(id=str(result.id), email=result.email, phone=result.phone,
                                 last_name=result.last_name, first_name=result.first_name,
                                 middle_name=result.middle_name)
            response = auth_pb2.ValidateTokenResponse(
                success_payload=user,
                error=False,
                status_code=status_code,
            )
            return response
        else:
            response = auth_pb2.ValidateTokenResponse(
                error_payload=result,
                error=True,
                status_code=status_code
            )
            return response


async def serve():
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server = aio.server()
    listen_addr = "[::]:9999"
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthServicer(), server)
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
