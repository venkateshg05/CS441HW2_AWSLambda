Venkatesh Gopalakrishnan (UIN: 655290219)

AWS Lambda APIs that processes log files on S3.

YouTube Documentation url: 

This project has two components to it:
  1) The Lambdas (FAAS) on AWS that processes the log files on an S3 storage
  2) The gRPC & HTTP clients that consume the exposed Lambda APIs
  
 Lambdas:
 
 There are 2 lambdas defined in this project.
  1) To check if the log files exist for the search time interval - accessed by the gRPC client
  2) To get the log files stored on s3 as md5 checksum for the given search time interval - accessed by Akka HTTP client
  
 These two lambdas are created using AWS SAM CLI as shown in the following steps:
  1) run 'sam init' to initialize the lambda dir
  2) edit the app.py file to decide what the lambda handler will do
  3) edit the requirements.txt file to have all the req packages
  4) run 'sam build' to package the required libraries and the lambda function defined in app.py
  5) run 'sam deploy' to deploy the code on AWS Lambda
  6) The template.yaml file at the root directory declares the API route exposed by the lambda
  
 gRPC:
  The gRPC client & server are developed in python.
  1) Install the pygrpc & it's dependencies
  2) define the protobuf structure for the client & server comm. in a .proto file
  3) generate the stubs required to achieve the protobuf communication between the client & server
  4) define the server functionality in the grpc_server.py. The class LogProcessor connects to the lambda API & exposes the ip:port for the client to connect
  5) define the client functionality in the grpc_client.py. The client connects to the server ip and using the generated client stub, it connects to the server & passes the required parameters (start_time & time_delta). These two args are given as command line args when running the client.py file in the same order
  6) The server receives the parameters, unmarshalls them and does a HTTP call to the lambda API
  7) The lambda API returns whether the log files exist for the given time window
  
HTTP:
 The HTTP way of accessing the lambda API to retreive md5 checksum of the log files is realised using Akka HTTP framework.
 The Akka client is implemented in this repo: https://github.com/venkateshg05/AkkaHttpClient.git
 Below is the functionality of this HTTP client:
   1) Input: Gets the start_time & time delta as command line args (in that order)
   2) Connects to the lambda API on AWS
   3) Requests the logs between the start_time & time_delta as HTTP POST request
   4) Prints the results from the lambda
