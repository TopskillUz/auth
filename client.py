import grpc

import auth_pb2, auth_pb2_grpc


class AuthClient:
    def __init__(self, host='localhost', server_port=99998):
        self.host = host
        self.server_port = server_port

        self.channel = grpc.insecure_channel(f'{self.host}:{self.server_port}')
        self.stub = auth_pb2_grpc.AuthServiceStub(self.channel)

    def check_username(self, username):
        print("AuthClient send request")
        request = auth_pb2.CheckUsernameRequest(username=username)
        return self.stub.check_username(request=request)
