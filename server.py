import random
from concurrent import futures

import grpc

import auth_pb2_grpc, auth_pb2
from client import AuthClient


class AuthServicer(auth_pb2_grpc.AuthServiceServicer):

    def register(self, request, context):
        print("AuthServicer received request from GatewayClient")
        auth_client = AuthClient()

        resp = auth_client.check_username(request.username)

        if not bool(resp.value):
            user = auth_pb2.User(id=1, username=request.username, password=request.password, email=request.email)
            response = auth_pb2.RegisterUserResponse(
                success_payload=user,
                error=False,
                status_code=200,
            )
            return response
        else:
            response = auth_pb2.RegisterUserResponse(
                error_payload='This user already stored',
                error=True,
                status_code=400
            )
            return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthServicer(), server)
    server.add_insecure_port(f"[::]:99999")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
