# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import log_processor_lambda_pb2 as log__processor__lambda__pb2


class LogsProcessorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CheckLogsExists = channel.unary_unary(
                '/LogsProcessor/CheckLogsExists',
                request_serializer=log__processor__lambda__pb2.TimeWindow.SerializeToString,
                response_deserializer=log__processor__lambda__pb2.LambdaResult.FromString,
                )


class LogsProcessorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CheckLogsExists(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LogsProcessorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CheckLogsExists': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckLogsExists,
                    request_deserializer=log__processor__lambda__pb2.TimeWindow.FromString,
                    response_serializer=log__processor__lambda__pb2.LambdaResult.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'LogsProcessor', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LogsProcessor(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CheckLogsExists(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/LogsProcessor/CheckLogsExists',
            log__processor__lambda__pb2.TimeWindow.SerializeToString,
            log__processor__lambda__pb2.LambdaResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
