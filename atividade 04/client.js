const net = require("net");
const fs = require("fs");
const process = require("process");

if (process.argv.length !== 5) {
  console.log("Uso: node client.js <ip_servidor> <porta> <nome_arquivo>");
  process.exit(1);
}

const serverIP = process.argv[2];
const serverPort = process.argv[3];
const fileName = process.argv[4];

const client = new net.Socket();
client.connect(serverPort, serverIP, () => {
  console.log("Conectado ao servidor");
  client.write(fileName);
});

client.on("data", (data) => {
  const response = data.toString();
  if (response.startsWith("EXIST")) {
    const fileSize = parseInt(response.split(" ")[1]);
    console.log(`Arquivo encontrado. Tamanho: ${fileSize}`);
    client.write("OK");

    const fileStream = fs.createWriteStream(fileName);
    let receivedBytes = 0;
    client.on("data", (chunk) => {
      receivedBytes += chunk.length;
      const progress = (receivedBytes / fileSize) * 100;
      console.log(`Recebendo arquivo... ${progress.toFixed(2)}%`);
      fileStream.write(chunk);

      if (receivedBytes === fileSize) {
        console.log("Arquivo recebido com sucesso.");
        client.destroy();
      }
    });
  } else {
    console.log("Arquivo não encontrado.");
    client.destroy();
  }
});

client.on("close", () => {
  console.log("Conexão encerrada.");
});
