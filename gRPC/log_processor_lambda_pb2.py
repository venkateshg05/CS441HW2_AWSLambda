# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: log_processor_lambda.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1alog_processor_lambda.proto\"2\n\nTimeWindow\x12\x11\n\tstartTime\x18\x01 \x01(\t\x12\x11\n\ttimeDelta\x18\x02 \x01(\t\"\x1f\n\x0cLambdaResult\x12\x0f\n\x07message\x18\x01 \x01(\t2@\n\rLogsProcessor\x12/\n\x0f\x43heckLogsExists\x12\x0b.TimeWindow\x1a\r.LambdaResult\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'log_processor_lambda_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TIMEWINDOW._serialized_start=30
  _TIMEWINDOW._serialized_end=80
  _LAMBDARESULT._serialized_start=82
  _LAMBDARESULT._serialized_end=113
  _LOGSPROCESSOR._serialized_start=115
  _LOGSPROCESSOR._serialized_end=179
# @@protoc_insertion_point(module_scope)
