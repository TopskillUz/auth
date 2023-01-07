import os

import grpc

from grpc_generated_files import auth_pb2, auth_pb2_grpc


class AuthClient:
    service = os.environ.get('USER_SVC_ADDRESS', 'localhost:9998')

    def __init__(self, service=service):
        self.service = service
        self.channel = grpc.insecure_channel(service)
        self.stub = auth_pb2_grpc.AuthServiceStub(self.channel)

    def check_username(self, username):
        print("AuthClient send request")
        request = auth_pb2.CheckUsernameRequest(username=username)
        return self.stub.check_username(request=request)
