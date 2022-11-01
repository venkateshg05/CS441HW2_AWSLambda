import log_processor_lambda_pb2_grpc
import log_processor_lambda_pb2
import grpc
import requests
from concurrent import futures
from HelperUtils.create_logger import create_logger


class LogProcessor(log_processor_lambda_pb2_grpc.LogsProcessorServicer):

    """
    gets the request from the grpc client
    unmarshalls the protobuf data
    makes an API call to the Lambda on AWS
    gets the result from the Lambda
    marshalls the result into a protobuf object
    sends the response object back to the client
    """

    def __init__(self) -> None:
        super().__init__()
        self.logger = create_logger(__name__)

    def CheckLogsExists(self, request, context):
        url = 'https://iglc5ilpn7.execute-api.us-east-1.amazonaws.com/Prod/checktimewithinbounds'
        data = {'start_time': request.startTime,
                'time_delta': request.timeDelta}
        try:
            x = requests.post(url, json=data)
        except Exception as e:
            self.logger.exception("Error accessing the API")
        return log_processor_lambda_pb2.LambdaResult(
            message=x.text
        )


def serve():
    """
    sets up the grpc server on port 50051
    listens for the client requests
    """
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    log_processor_lambda_pb2_grpc.add_LogsProcessorServicer_to_server(
        LogProcessor(), server
    )
    server.add_insecure_port('[::]:' + port)
    server.start()
    logger = create_logger(__name__)
    logger.info(f"Server started, listening on {port}")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
