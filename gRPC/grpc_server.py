from concurrent import futures
import logging

import requests
import grpc
import log_processor_lambda_pb2
import log_processor_lambda_pb2_grpc


class LogProcessor(log_processor_lambda_pb2_grpc.LogsProcessorServicer):

    def CheckLogsExists(self, request, context):
        url = 'https://iglc5ilpn7.execute-api.us-east-1.amazonaws.com/Prod/checktimewithinbounds'
        data = {'start_time': request.startTime,
                'time_delta': request.timeDelta}
        x = requests.post(url, json=data)
        return log_processor_lambda_pb2.LambdaResult(
            message=x.text
        )


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    log_processor_lambda_pb2_grpc.add_LogsProcessorServicer_to_server(
        LogProcessor(), server
    )
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
