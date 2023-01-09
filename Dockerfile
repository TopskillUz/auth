FROM python:3.10-slim-bullseye
#FROM gcr.io/google_appengine/python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


#RUN pip install grpcio grpcio-tools

RUN mkdir /service
WORKDIR /service

COPY ./protos /service/protos/
COPY . /service/

RUN pip install --upgrade pip && pip install -r requirements.txt

#RUN python -m grpc_tools.protoc -I protos --python_out=grpc_generated_files --grpc_python_out=grpc_generated_files protos/*.proto

EXPOSE 9999

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["sh", "/entrypoint.sh"]
