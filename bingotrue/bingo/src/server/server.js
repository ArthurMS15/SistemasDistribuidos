const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const services = require('./services');

const PROTO_PATH = './bingo.proto';
const host = '127.0.0.1:50051';

const options = {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
};
const packageDefinition = protoLoader.loadSync(PROTO_PATH, options);
const bingoProto = grpc.loadPackageDefinition(packageDefinition);
const server = new grpc.Server();

server.addService(bingoProto.Bingo.service, services);

server.bindAsync(
  host,
  grpc.ServerCredentials.createInsecure(),
  () => {
    console.log(`Server running at http://${host}`);
    server.start();
  }
);
