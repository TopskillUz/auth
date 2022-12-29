import os

import grpc

import auth_pb2, auth_pb2_grpc


class AuthClient:
    user_host = os.environ.get('USER_HOST', 'localhost')

    def __init__(self, host=user_host, server_port=9998):
        self.host = host
        self.server_port = server_port

        self.channel = grpc.insecure_channel(f'{self.host}:{self.server_port}')
        self.stub = auth_pb2_grpc.AuthServiceStub(self.channel)

    def check_username(self, username):
        print("AuthClient send request")
        request = auth_pb2.CheckUsernameRequest(username=username)
        return self.stub.check_username(request=request)
