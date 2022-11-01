from __future__ import print_function
import log_processor_lambda_pb2_grpc
import log_processor_lambda_pb2
import grpc

from HelperUtils.create_logger import create_logger

logger = create_logger(__name__)


def run():

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = log_processor_lambda_pb2_grpc.LogsProcessorStub(channel)
        response = stub.CheckLogsExists(
            log_processor_lambda_pb2.TimeWindow(
                startTime='22-45', timeDelta='5'
            )
        )
    logger.info(f"Greeter client received: {response.message}")


if __name__ == '__main__':
    run()
