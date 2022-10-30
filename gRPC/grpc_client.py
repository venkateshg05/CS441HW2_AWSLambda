from __future__ import print_function

import logging

import grpc
import log_processor_lambda_pb2
import log_processor_lambda_pb2_grpc


def run():

    print("Will try to greet world ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = log_processor_lambda_pb2_grpc.LogsProcessorStub(channel)
        response = stub.CheckLogsExists(
            log_processor_lambda_pb2.TimeWindow(
                startTime='22-45', timeDelta='5'
            )
        )
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
