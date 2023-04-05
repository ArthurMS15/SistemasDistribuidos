const net = require("net");
const fs = require("fs");
const process = require("process");

/*net, criar um cliente de rede e se comunicar com o servidor.
fs, criar e manipular arquivos no sistema de arquivos local.
process, acessar argumentos da linha de comando e sair do programa.*/

if (process.argv.length !== 5) {
  console.log("Uso: node client.js <ip_servidor> <porta> <nome_arquivo>");  //quantidade correta de argumentos foi fornecia
  process.exit(1);
}

const serverIP = process.argv[2]; //armazena o segundo argumento
const serverPort = process.argv[3];
const fileName = process.argv[4];

const client = new net.Socket();  //cria um novo objeto de socket para o cliente.
client.connect(serverPort, serverIP, () => {
  console.log("Conectado ao servidor");
  client.write(fileName);
}); //conecta-se ao servidor no IP e porta especificados

client.on("data", (data) => { //define uma função de callback para lidar com os dados recebidos do servidor.
  const response = data.toString(); //converte os dados recebidos em uma string.
  if (response.startsWith("EXIST")) {
    const fileSize = parseInt(response.split(" ")[1]);
    console.log(`Arquivo encontrado. Tamanho: ${fileSize}`);
    client.write("OK");

    const fileStream = fs.createWriteStream(fileName); //cria um novo arquivo usando o nome fornecido e cria um fluxo de gravação para o arquivo.
    let receivedBytes = 0;
    client.on("data", (chunk) => {
      receivedBytes += chunk.length;
      const progress = (receivedBytes / fileSize) * 100;
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

//node client.js 127.0.0.1 1234 arquivo.txt
